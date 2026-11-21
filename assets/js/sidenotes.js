(function () {
  const article = document.querySelector('article.with-sidenotes');
  if (!article) return;

  const defsContainer = article.querySelector('.footnotes');
  if (!defsContainer) return;

  // Must match $sidenote-breakpoint in _sass/sidenotes.sass
  const wideQuery = window.matchMedia('(min-width: 70rem)');

  const defs = {};
  defsContainer.querySelectorAll('li[id^="fn:"]').forEach(function (li) {
    const clone = li.cloneNode(true);
    clone.querySelectorAll('.reversefootnote').forEach(function (a) {
      a.remove();
    });
    defs[li.id] = clone;
  });

  const refs = Array.from(article.querySelectorAll('sup[id^="fnref"]'));
  if (!refs.length) return;

  // Build the note's contents: number label + a copy of the footnote body.
  function buildNoteContent(container, numText, def) {
    const num = document.createElement('span');
    num.className = 'sidenote-num';
    num.textContent = numText;

    const body = document.createElement('span');
    body.className = 'sidenote-body';
    Array.from(def.childNodes).forEach(function (n) {
      body.appendChild(n.cloneNode(true));
    });

    const firstP = body.querySelector('p');
    if (firstP) {
      firstP.insertBefore(num, firstP.firstChild);
      container.appendChild(body);
    } else {
      container.appendChild(num);
      container.appendChild(body);
    }
  }

  const blockSelector = 'p, li, blockquote, h1, h2, h3, h4, h5, h6, pre, figure';
  const groups = new Map();
  refs.forEach(function (ref) {
    const block = ref.closest(blockSelector);
    if (!block || !article.contains(block)) return;
    if (!groups.has(block)) groups.set(block, []);
    groups.get(block).push(ref);
  });

  const asides = [];
  const asideLinks = new Map(); // aside -> marker links it holds

  function setExpanded(link, open) {
    link.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  function setAside(aside, open) {
    aside.classList.toggle('expanded', open);
    (asideLinks.get(aside) || []).forEach(function (l) { setExpanded(l, open); });
  }

  groups.forEach(function (refsInBlock, block) {
    // Wide screens: one margin note group per paragraph.
    const aside = document.createElement('aside');
    aside.className = 'sidenote-group';
    asideLinks.set(aside, []);

    // Narrow screens: one inline note per marker, placed after the paragraph
    // (or at the end of a list item, so the markup stays valid).
    let insertAfter = block;

    refsInBlock.forEach(function (ref) {
      const link = ref.querySelector('a[href^="#fn:"]');
      if (!link) return;
      const defId = link.getAttribute('href').slice(1);
      const def = defs[defId];
      if (!def) return;
      const numText = (ref.textContent || '').trim();

      const note = document.createElement('div');
      note.className = 'sidenote';
      buildNoteContent(note, numText, def);
      aside.appendChild(note);
      asideLinks.get(aside).push(link);

      const inline = document.createElement('div');
      inline.className = 'sidenote-inline';
      inline.id = 'sn-inline-' + defId.replace(/[^\w-]/g, '-');
      const inner = document.createElement('div');
      inner.className = 'sidenote-inline-inner';
      const card = document.createElement('div');
      card.className = 'sidenote-inline-card';
      card.setAttribute('role', 'note');
      buildNoteContent(card, numText, def);
      inner.appendChild(card);
      inline.appendChild(inner);

      if (block.tagName === 'LI' && insertAfter === block) {
        block.appendChild(inline);
      } else {
        insertAfter.insertAdjacentElement('afterend', inline);
      }
      insertAfter = inline;

      link.setAttribute('role', 'button');
      link.setAttribute('aria-expanded', 'false');
      link.setAttribute('aria-controls', inline.id);
      link.setAttribute('aria-label', 'Note ' + numText);

      link.addEventListener('click', function (e) {
        e.preventDefault();
        if (wideQuery.matches) {
          setAside(aside, !aside.classList.contains('expanded'));
        } else {
          const open = !inline.classList.contains('open');
          inline.classList.toggle('open', open);
          setExpanded(link, open);
        }
      });
    });

    article.appendChild(aside);
    asides.push({ aside: aside, block: block });

    aside.addEventListener('click', function (e) {
      if (e.target.closest('a')) return;
      setAside(aside, !aside.classList.contains('expanded'));
    });
  });

  // Crossing the breakpoint: close everything so marker state stays truthful.
  wideQuery.addEventListener('change', function () {
    article.querySelectorAll('.sidenote-inline.open').forEach(function (el) {
      el.classList.remove('open');
    });
    asides.forEach(function (entry) { setAside(entry.aside, false); });
  });

  function positionAll() {
    const articleRect = article.getBoundingClientRect();
    asides.forEach(function (entry) {
      const blockRect = entry.block.getBoundingClientRect();
      entry.aside.style.top = (blockRect.top - articleRect.top) + 'px';
    });
  }

  positionAll();
  window.addEventListener('resize', positionAll);
  window.addEventListener('load', positionAll);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(positionAll);
  }
})();
