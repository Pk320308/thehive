(function() {
    'use strict';
    angular.module('cynoxControllers')
        .directive('mainSidebar', function() {
            return {
                restrict: 'E',
                templateUrl: 'views/components/main-sidebar.component.html'
            };
        });
})();
