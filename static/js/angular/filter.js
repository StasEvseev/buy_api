angular.module("FilterApp", [])
.filter('propsFilter', function() {
  return function(items, props) {
    var out = [];

    if (angular.isArray(items)) {
      items.forEach(function(item) {
        var itemMatches = false;

        var keys = Object.keys(props);
        for (var i = 0; i < keys.length; i++) {
          var prop = keys[i];
          var text = props[prop].toLowerCase();
          if (item[prop].toString().toLowerCase().indexOf(text) !== -1) {
            itemMatches = true;
            break;
          }
        }

        if (itemMatches) {
          out.push(item);
        }
      });
    } else {
      // Let the output be the input untouched
      out = items;
    }

    return out;
  }
})
.filter('propsFilterDict', function() {
    return function(items, props) {
        var out = [];
        var text = props[0].toLowerCase();
        var property = props[1];
        if (angular.isArray(items)) {
            items.forEach(function(item) {
                var itemMatches = false;

                for (var i = 0; i < property.length; i++) {
                    var prop = property[i];
                    if (item[prop].toString().toLowerCase().indexOf(text) !== -1) {
                        itemMatches = true;
                        break;
                    }
                }

                if (itemMatches) {
                    out.push(item);
                }
            });
        } else {
          // Let the output be the input untouched
            out = items;
        }

        return out;
    }
})

.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
})
.filter('rub', function() {
  return function(input) {
      if (_.isNaN(input)) {
          return "";
      }
      else if (_.isNull(input)) {
          return "";
      }
      else if (_.isUndefined(input)) {
          return "";
      }
      else if (input == "") {
          return "";
      }
       else {
          return parseFloat(input).toFixed(2) + " руб.";
      }
      //return input;
  };
});