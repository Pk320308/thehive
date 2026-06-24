(function() {
    'use strict';

    angular.module('cynoxComponents')
        .component('observableFlags', {
            controller: function() {
                this.filterBy = function(fieldName, newValue) {
                    this.onFilter({
                        fieldName: fieldName,
                        value: newValue
                    });
                };
            },
            controllerAs: '$ctrl',
            templateUrl: 'views/components/common/observable-flags.component.html',
            bindings: {
                observable: '<',
                inline: '<',
                hideSimilarity: '<',
                hideSeen: '<',
                hideTlp: '<',
                onFilter: '&'
            }
        });
})();
