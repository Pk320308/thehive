(function() {
    'use strict';
    angular.module('cynoxDirectives').directive('tagList', function() {
        return {
            restrict: 'E',
            scope: {
                data: '='
            },
            templateUrl: 'views/directives/tag-list.html'
        };
    });

})();
