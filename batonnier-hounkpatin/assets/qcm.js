/* QCM « faits ou opinions » (page 21) : classement d'énoncés, réponse et explication immédiates, score local.
   Aucune donnée n'est conservée ni transmise : l'état disparaît à la fermeture de la page. */
(function () {
  'use strict';
  var root = document.getElementById('qcm');
  if (!root || /[?&]pdf\b/.test(location.search)) return;
  var CAT = { F: 'Fait étayé', N: 'Fait non étayé ou contredit', O: 'Opinion ou supposition', Q: 'Qualification juridique' };
  var items = Array.prototype.slice.call(root.querySelectorAll('.qitem'));
  var txt = root.querySelector('.qtxt'), jauge = root.querySelector('.qjauge i');
  var res = root.querySelector('.qres'), reset = document.getElementById('qreset');
  var done = 0, good = 0, stat = {};
  root.classList.add('js');

  function maj() {
    txt.textContent = done + ' / ' + items.length + ' · ' + good + ' bien classé' + (good > 1 ? 's' : '');
    jauge.style.width = (100 * done / items.length) + '%';
    if (done === items.length) fin();
  }

  function fin() {
    var h = '<h3>Votre résultat : ' + good + ' énoncé' + (good > 1 ? 's' : '') + ' bien classé' + (good > 1 ? 's' : '') + ' sur ' + items.length + '</h3>';
    h += '<table><thead><tr><th>Catégorie</th><th>Énoncés</th><th>Bien classés</th></tr></thead><tbody>';
    Object.keys(CAT).forEach(function (k) {
      var s = stat[k] || { n: 0, g: 0 };
      h += '<tr><td>' + CAT[k] + '</td><td>' + s.n + '</td><td>' + s.g + '</td></tr>';
    });
    h += '</tbody></table>';
    h += '<p>Ce tri est celui que l\'enquêteur devait faire : constater ce qui se prouve, sans confondre ce qui se croit avec ce qui se constate. Le raisonnement qui en découle est exposé plus bas : <a href="#bilan">ce que votre classement établit</a>.</p>';
    res.innerHTML = h;
    res.hidden = false;
    reset.hidden = false;
    res.focus();
  }

  function rep(it, k, b) {
    if (it.getAttribute('data-done')) return;
    it.setAttribute('data-done', '1');
    var c = it.getAttribute('data-c'), ok = (k === c);
    done++; if (ok) good++;
    var s = stat[c] || (stat[c] = { n: 0, g: 0 }); s.n++; if (ok) s.g++;
    Array.prototype.forEach.call(it.querySelectorAll('.qbtn'), function (x) {
      x.disabled = true;
      x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
      if (x.getAttribute('data-k') === c) x.classList.add('good');
    });
    b.classList.add(ok ? 'ok' : 'ko');
    it.classList.add('fait', ok ? 'bon' : 'mauvais');
    it.querySelector('.qverdict').innerHTML = '<b>' + (ok ? 'Bien classé. ' : 'Pas tout à fait. ') + 'Réponse : ' + CAT[c] + '.</b>';
    maj();
  }

  items.forEach(function (it) {
    var box = it.querySelector('.qbtns');
    Object.keys(CAT).forEach(function (k) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'qbtn'; b.setAttribute('data-k', k); b.textContent = CAT[k];
      b.addEventListener('click', function () { rep(it, k, b); });
      box.appendChild(b);
    });
  });
  reset.addEventListener('click', function () { location.reload(); });
  maj();
})();
