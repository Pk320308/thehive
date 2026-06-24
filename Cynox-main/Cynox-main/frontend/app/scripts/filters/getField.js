(function() {
    'use strict';
    angular.module('cynoxFilters').filter('getField', function() {
        return function(obj, param) {
            if (obj !== undefined && obj !== null) {
                return obj[param];
            } else {
                return '';
            }
        };
    });
})();
