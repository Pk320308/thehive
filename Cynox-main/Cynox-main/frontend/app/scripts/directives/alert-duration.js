(function() {
    'use strict';
    angular.module('cynoxDirectives').directive('alertDuration', function() {
        return {
            restrict: 'E',
            scope: {
                start: '=',
                end: '=',
                icon: '@',
                indicator: '='
            },
            templateUrl: 'views/directives/alert-duration.html'
        };
    });
})();
