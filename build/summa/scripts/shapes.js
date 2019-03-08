// copied from http://williamsharkey.com/Shapes.html

var polyText = "";
/*
a.value = rgb2hex(getCSSRule('.a').style.fill);
b.value = rgb2hex(getCSSRule('.b').style.fill);
c.value = rgb2hex(getCSSRule('.c').style.fill);
d.value = rgb2hex(getCSSRule('.d').style.fill);
e.value = rgb2hex(getCSSRule('.e').style.fill);
f.value = rgb2hex(getCSSRule('.f').style.fill);
at.value = getCSSRule('.a').style.fillOpacity;
bt.value = getCSSRule('.b').style.fillOpacity;
ct.value = getCSSRule('.c').style.fillOpacity;
dt.value = getCSSRule('.d').style.fillOpacity;
et.value = getCSSRule('.e').style.fillOpacity;
ft.value = getCSSRule('.f').style.fillOpacity;
*/
var cssText = "";
function rgb2hex(rgb) {
  return '#' + rgb
    .replace("rgb(", "")
    .replace("rgba(", "")
    .replace(")", "")
    .split(", ")
    .splice(0, 3).map(function (x) { var hex = parseInt(x).toString(16); return hex.length == 1 ? "0" + hex : hex; })
    .join('');
}
function updateCssText() {
  var c = '<style>\n  ';
  c += innerCssText();
  c += "</style>\n";
  cssText = c;
}
function innerCssText() {
  var c = '';
  c += getCSSRule('.a').cssText
    //.replace('opacity: 1; ', '')
    + '\n  ';
  c += getCSSRule('.b').cssText + '\n  ';
  c += getCSSRule('.c').cssText + '\n  ';
  c += getCSSRule('.d').cssText + '\n  ';
  c += getCSSRule('.e').cssText + '\n  ';
  c += getCSSRule('.f').cssText + '\n';

  return c;
}
function changeBackground(v, cls) {
  getCSSRule('.' + cls).style.fill = v;
  updateCssText();
  updateTextBox();
}
function changeOpacity(v, cls) {
  getCSSRule('.' + cls).style.fillOpacity = v;
  updateCssText();
  updateTextBox();
}
function getCSSRule(ruleName) {
  ruleName = ruleName.toLowerCase();
  var styleSheet;
  var i, ii;
  var cssRule = false;
  var cssRules;
  for (i = 0; i < document.styleSheets.length; i++) {
    styleSheet = document.styleSheets[i];
    if (!styleSheet.href) {
      if (styleSheet.cssRules) {
        cssRules = styleSheet.cssRules;
      } else {
        cssRules = styleSheet.rules;
      }
      for (ii = 0; ii < cssRules.length; ii++) {
        cssRule = cssRules[ii];
        if (cssRule) {
          if (cssRule.selectorText) {
            if (cssRule.selectorText.toLowerCase() == ruleName) {
              return cssRule;
            }
          }
        }
      }
    }
  }
  return null;
}
var colors = "a b c d e f".split(" ");
var points = ['3 6', '3 0', '6 4', '6 2', '0 4', '0 2'];
var nums = "0 2 4".split(" ");
var rads = "2".split(" ");
var objects = 12;
var circleChance = 0;
var longPolyChance = 0;
var pointsChance = 1;
var svgStart = "<svg viewBox='0 0 6 6' xmlns='http://www.w3.org/2000/svg'>\n";
var svgEnd = "</svg>";
function templateGen() {

  var template = '';
  for (var p = 0; p < objects; p++) {
    if (Math.random() < circleChance) {
      template += "  <circle  class='^' cx='_' cy='_' r='$' />\n";
    } else if (Math.random() < longPolyChance) {
      template += "  <polygon class='^' points='P P P P'/>\n";
    } else if (Math.random() < pointsChance) {
      template += "  <polygon class='^' points='P P P'/>\n";
    } else {
      template += "  <polygon class='^' points='_ _ _ _ _ _'/>\n";
    }
  }
  return template;
}
function newShape() {
    var t = templateGen();
    t = replace(t, '_', nums);
    t = replace(t, '$', rads);
    t = replace(t, 'P', points);
    t = replace(t, '^', colors);
    return svgStart + t + svgEnd;
}
function replace(t, match, arr) {
  while (t.indexOf(match) > -1) {
    var x = Math.floor(Math.random() * arr.length);
    t = t.replace(match, arr[x]);
  }
  return t;
}

function composedPath(el) {

  var path = [];

  while (el) {

    path.push(el);

    if (el.tagName === 'HTML') {

      path.push(document);
      path.push(window);

      return path;
    }

    el = el.parentElement;
  }
}

function saveClick(e) {
  var path = e.path || (e.composedPath && e.composedPath() || composedPath(e.target));
  var matches = path.filter(function (y) {
    return y.tagName === "svg";
  });
  if (matches.length !== 1) return;
  clickedSvg = matches[0];



  var fromToolsMatches = path.filter(function (y) {
    if (y.tagName === "TR") {
      y.querySelector('input[type="color"]').click();
    }

    return y.tagName === "TOOLS";
  });
  var fromTools = fromToolsMatches.length > 0

  if (fromTools) {
    return;
  }

  var fromSavedSection = path.filter(function (y) {
    return y.id === "saved";
  });
  var underReview = fromSavedSection.length > 0



  if (underReview) {
    saveClick2(clickedSvg, underReview);
  } else {


    saveClick2(clickedSvg, underReview);
  }

}
function saveClick2(m, underReview) {

  if (!m) {
    m = clickedSvg;
  }


  if (!underReview) {

    var d = document.createElement('div')
    m.parentNode.insertBefore(d, m);
    document.querySelector('#saved').appendChild(m);
    d.style.backgroundImage = getBackground(m);
  } else {
    polyText = m.outerHTML;
    updateTextBox(m);
  }

}

function getBackground(svg) {

  var styleEl = document.createElement('style');

  styleEl.innerHTML = innerCssText();
  var x = svg.cloneNode(true);

  x.appendChild(styleEl);
  var data = 'data:image/svg+xml;charset=UTF-8,' + escape(x.outerHTML);
  var bg = "url('" + data + "')";
  return bg
}

var ta = document.querySelector('textarea');

function updateTextBox(m) {
  if (!m) {
    m = clickedSvg;
  }

  var styleEl = document.createElement('style');

  styleEl.innerHTML = innerCssText();
  var newJoined = m.cloneNode(true);

  newJoined.appendChild(styleEl);
  //var joined = svgStart + cssText + polyText + svgEnd;


  ta.value = newJoined.outerHTML;

  var data = 'data:image/svg+xml;charset=UTF-8,' + escape(newJoined.outerHTML);
  //var x = "url('" + data + "')";

  //ta.style.backgroundImage = x


  download.setAttribute('href', data);
}
