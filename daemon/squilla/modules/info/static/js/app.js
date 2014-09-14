
squilla_app.config(['$routeProvider', function($routeProvider) {

        $routeProvider.when('/info/network', {templateUrl: '/static/info/partials/networks.html', controller: 'NetworkCtrl'});

    }]);


