(function() {
    'use strict';
    angular.module('cynoxControllers')
        .directive('header', function() {
            return {
                restrict: 'E',
                templateUrl: 'views/components/header.component.html'
            };
        });
})();
