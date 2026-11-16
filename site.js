'use strict';
(() => {
  const input = document.getElementById('sweet-search');
  if (input) {
    const panel = document.querySelector('.search-results');
    const items = Array.from(document.querySelectorAll('.search-result'));
    const status = document.getElementById('search-status');
    const normalize = s => s.normalize('NFKC').toLocaleLowerCase('ja').replace(/\s+/g, '');
    const update = () => {
      const q = normalize(input.value.trim());
      panel.hidden = !q;
      let total = 0;
      for (const item of items) {
        const match = q && normalize(item.dataset.search).includes(q);
        item.hidden = !match;
        total += Number(Boolean(match));
      }
      status.textContent = !q ? '' : total ? `${total}種類のお菓子が見つかりました。` : '該当するお菓子がありません。別の名前や素材でも探してみてください。';
    };
    input.addEventListener('input', update);
    update();
  }
  const filters = Array.from(document.querySelectorAll('[data-budget]'));
  if (filters.length) {
    const products = Array.from(document.querySelectorAll('.product[data-price]'));
    const status = document.getElementById('budget-status');
    const allowed = ['all', '1000', '2000', '3000', 'over'];
    const update = budget => {
      let total = 0;
      for (const p of products) {
        const price = Number(p.dataset.price);
        const show = budget === 'all' || (budget === 'over' ? price > 3000 : price > 0 && price <= Number(budget));
        p.hidden = !show;
        total += Number(show);
      }
      for (const b of filters) b.setAttribute('aria-pressed', String(b.dataset.budget === budget));
      // Keep the contents index synchronized with the visible product cards.
      for (const a of document.querySelectorAll('.page-index a')) {
        const product = document.getElementById(a.hash.slice(1));
        if (product) a.closest('li').hidden = product.hidden;
      }
      status.textContent = `${total}商品を表示しています。価格は確認時の目安です。`;
    };
    for (const b of filters) b.addEventListener('click', () => update(b.dataset.budget));
    const initial = new URLSearchParams(location.search).get('budget') || 'all';
    update(allowed.includes(initial) ? initial : 'all');
  }
})();
