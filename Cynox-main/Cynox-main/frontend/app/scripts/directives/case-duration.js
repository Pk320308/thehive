(function() {
    'use strict';
    angular.module('cynoxDirectives').directive('caseDuration', function() {
        return {
            restrict: 'E',
            scope: {
                start: '=',
                end: '=',
                icon: '@',
                indicator: '='
            },
            templateUrl: 'views/directives/case-duration.html'
        };
    });
})();
