(function() {
    'use strict';
    angular.module('cynoxFilters').filter('sha256', function() {
        return function(value) {
            if(!value) {
                return '';
            }

            return CryptoJS.SHA256(value).toString();
        };
    });
})();
