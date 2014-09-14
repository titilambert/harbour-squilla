
squilla_app.config(['$routeProvider', function($routeProvider) {

        $routeProvider.when('/system/network', {templateUrl: '/static/system/partials/networks.html', controller: 'NetworkCtrl'});

    }]);


