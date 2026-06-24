(function() {
    'use strict';
    angular.module('cynoxFilters').filter('percentage', function($filter) {
        return function(input, decimals) {
            return $filter('number')(input * 100, decimals) + '%';
        };
    });
})();
