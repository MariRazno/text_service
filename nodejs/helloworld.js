'use strict';
/* global eopti */

(async function() {

  await require('eopti/ms/ms_lib.js');

  function sayHello() {

    try {

      return "Hallo aus der Microservice helloworld um: " + (new Date()) ;

    } catch (errorMsg) {
      throw errorMsg + "<pre> << helloworld.sayHello";
    }
  }

  function echo(request) {

    try {

      return {
        "msg" :  "Echo aus der Microservice helloworld um: " + (new Date()),
        "echo" : request
      }

    } catch (errorMsg) {
      throw errorMsg + "<pre> << helloworld.echo";
    }
  }


  await eopti.ms.start({

    "hello" : sayHello,

    "echo" : echo

  });

})();

