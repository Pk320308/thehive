(function() {
    'use strict';
    angular.module('cynoxFilters').filter('fang', function(UtilsSrv) {
        return function(value) {
            if(!value) {
                return '';
            }

            return UtilsSrv.fangValue(value);
        };
    });
})();
