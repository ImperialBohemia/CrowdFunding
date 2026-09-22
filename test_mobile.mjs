import { spawn } from 'child_process';

const port = 9222;
const chrome = spawn('google-chrome', [
  '--headless=new',
  '--disable-gpu',
  `--remote-debugging-port=${port}`,
  'file:///home/q/CrowdFunding/index.html'
]);

await new Promise(resolve => setTimeout(resolve, 1500));

try {
  const resp = await fetch(`http://127.0.0.1:${port}/json`);
  const tabs = await resp.json();
  const target = tabs.find(t => t.url.includes('index.html')) || tabs[0];
  const ws = new WebSocket(target.webSocketDebuggerUrl);

  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });

  let id = 1;
  const send = (method, params = {}) => {
    return new Promise((resolve) => {
      const msgId = id++;
      const handler = (event) => {
        const data = JSON.parse(event.data);
        if (data.id === msgId) {
          ws.removeEventListener('message', handler);
          resolve(data.result);
        }
      };
      ws.addEventListener('message', handler);
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
  };

  const viewports = [
    { name: 'iPhone SE (Old/Smallest)', width: 320, height: 568 },
    { name: 'Galaxy / Small Android', width: 360, height: 640 },
    { name: 'iPhone Standard (12/13/14)', width: 375, height: 812 },
    { name: 'Android Modern (Pixel/Galaxy)', width: 412, height: 915 }
  ];

  console.log('=== SPOUŠTÍM TESTY MOBILE-FRIENDLY PRO index.html ===\n');

  for (const vp of viewports) {
    await send('Emulation.setDeviceMetricsOverride', {
      width: vp.width,
      height: vp.height,
      deviceScaleFactor: 2,
      mobile: true
    });

    const res = await send('Runtime.evaluate', {
      expression: `(() => {
        const bodyWidth = document.body.offsetWidth;
        const scrollWidth = document.documentElement.scrollWidth;
        const innerWidth = window.innerWidth;
        const hasHorizontalOverflow = scrollWidth > innerWidth;

        // Check buttons / inputs tap target heights
        const buttons = Array.from(document.querySelectorAll('button, a.btn-action-cta, a.sticky-btn, .amount-btn'));
        const smallTapTargets = buttons.filter(b => {
          const rect = b.getBoundingClientRect();
          return rect.height < 40 && b.offsetParent !== null;
        }).map(b => ({ tag: b.tagName, text: b.innerText.trim().slice(0, 20), height: b.getBoundingClientRect().height }));

        // Check font sizes for inputs (iOS auto-zoom prevention requires >= 16px)
        const inputs = Array.from(document.querySelectorAll('input, select, textarea'));
        const smallInputs = inputs.filter(i => {
          const fontSize = parseFloat(window.getComputedStyle(i).fontSize);
          return fontSize < 16;
        }).map(i => ({ id: i.id, fontSize: window.getComputedStyle(i).fontSize }));

        return {
          viewport: innerWidth,
          scrollWidth,
          hasHorizontalOverflow,
          smallTapTargetsCount: smallTapTargets.length,
          smallTapTargets,
          smallInputsCount: smallInputs.length,
          smallInputs
        };
      })()`,
      returnByValue: true
    });

    const test = res?.result?.value || res?.value || {};

    console.log(`[TEST] Viewport: ${vp.name} (${vp.width}x${vp.height})`);
    console.log(`  - Horizontální přetékání (overflow): ${test.hasHorizontalOverflow ? 'CHYBA (přetéká: ' + test.scrollWidth + 'px > ' + test.viewport + 'px)' : 'V POŘÁDKU (žádný boční scroll)'}`);
    console.log(`  - Malé klikací prvky (<40px výška): ${test.smallTapTargetsCount === 0 ? 'V POŘÁDKU (všechny splňují)' : test.smallTapTargetsCount + ' prvků'}`);
    if (test.smallTapTargets?.length) {
      test.smallTapTargets.forEach(t => console.log(`      * ${t.tag} "${t.text}" (výška: ${Math.round(t.height)}px)`));
    }
    console.log(`  - Vstupní pole písmo (<16px iOS zoom risk): ${test.smallInputsCount === 0 ? 'V POŘÁDKU (>=16px)' : test.smallInputsCount + ' polí pod 16px'}`);
    if (test.smallInputs?.length) {
      test.smallInputs.forEach(i => console.log(`      * Input #${i.id} (písmo: ${i.fontSize})`));
    }
    console.log('');
  }

  ws.close();

} finally {
  chrome.kill();
}
