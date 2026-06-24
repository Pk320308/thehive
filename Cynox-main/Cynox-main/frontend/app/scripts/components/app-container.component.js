(function() {
    'use strict';
    angular.module('cynoxControllers')
        .directive('appContainer', function() {
            return {
                restrict: 'E',
                templateUrl: 'views/components/app-container.component.html'
            };
        });
})();
