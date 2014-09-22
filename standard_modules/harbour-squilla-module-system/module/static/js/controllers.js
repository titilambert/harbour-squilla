

squilla_controllers.controller('SystemNetworkCtrl', ['$scope', '$http',
        function($scope, $http) {
            $http.get('/system/networks').success(function(data) {
                $scope.networks = data['networks'];
            });
    }]);


