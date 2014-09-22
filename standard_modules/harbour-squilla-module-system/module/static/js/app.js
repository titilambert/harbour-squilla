
squilla_app.config(['$routeProvider', function($routeProvider) {

        $routeProvider.when('/system/network', {templateUrl: '/static/harbour-squilla-module-system/partials/networks.html', controller: 'SystemNetworkCtrl'});

    }]);


