(function() {
    'use strict';
    angular.module('cynoxDirectives')
        .directive('psearch', function() {
            return {
                'restrict': 'E',
                'templateUrl': 'views/directives/psearch.html',
                'scope': {
                    'control': '='
                }
            };
        });
})();
