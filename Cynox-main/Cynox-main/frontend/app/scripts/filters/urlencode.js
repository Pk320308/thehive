(function() {
    'use strict';

    angular.module('cynoxFilters').filter('escape', function() {
        return window.encodeURIComponent;
    });
})();
