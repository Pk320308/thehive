(function() {
    'use strict';
    angular.module('cynoxDirectives')
        .directive('updatableSelect', function(UtilsSrv) {
            return {
                'restrict': 'E',
                'link': UtilsSrv.updatableLink,
                'templateUrl': 'views/directives/updatable-select.html',
                'scope': {
                    'options': '=?',
                    'value': '=?',
                    'onUpdate': '&',
                    'active': '=?',
                    'placeholder': '@',
                    'clearable': '<?'
                }
            };
        });
})();
