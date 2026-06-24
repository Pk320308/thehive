(function() {
    'use strict';
    angular.module('cynoxDirectives')
        .directive('permissionList', function() {
            return {
                restrict: 'E',
                templateUrl: 'views/directives/permission-list.html',
                scope: {
                    permissions: '=',
                    showLabel: '=',
                    label: '='
                }
            };
        });
})();
