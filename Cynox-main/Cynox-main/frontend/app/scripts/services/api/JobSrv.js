(function() {
    'use strict';
    angular.module('cynoxServices')
        .factory('JobSrv', function($resource) {
            return $resource('./api/case/artifact/:artifactId/job/:analyzerId', {}, {}, {});
        });
})();
