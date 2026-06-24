(function() {
    'use strict';
    angular.module('cynoxControllers')
        .directive('controlSidebar', function() {
            return {
                restrict: 'E',
                templateUrl: 'views/components/control-sidebar.component.html'
            };
        });
})();
