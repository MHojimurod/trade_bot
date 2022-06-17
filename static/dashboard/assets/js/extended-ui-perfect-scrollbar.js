/**
 * Perfect Scrollbar
 */
'use strict';

document.addEventListener('DOMContentLoaded', function () {
  (function () {
    const verticalExample = document.getElementById('vertical-example'),
      horizontalExample = document.getElementById('horizontal-example'),
      horizVertExample = document.getElementById('both-scrollbars-example');

    // Vertical Example
    // BarchasiBarchasiBarchasiBarchasiBarchasiBarchasiBarchasi-----
    if (verticalExample) {
      new PerfectScrollbar(verticalExample, {
        wheelPropagation: false
      });
    }

    // Horizontal Example
    // BarchasiBarchasiBarchasiBarchasiBarchasiBarchasiBarchasi-----
    if (horizontalExample) {
      new PerfectScrollbar(horizontalExample, {
        wheelPropagation: false,
        suppressScrollY: true
      });
    }

    // Both vertical and Horizontal Example
    // BarchasiBarchasiBarchasiBarchasiBarchasiBarchasiBarchasi-----
    if (horizVertExample) {
      new PerfectScrollbar(horizVertExample, {
        wheelPropagation: false
      });
    }
  })();
});
