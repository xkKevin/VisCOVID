var lambdaDataprocessInterface =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/main.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./dist/componentClasses.json":
/*!************************************!*\
  !*** ./dist/componentClasses.json ***!
  \************************************/
/*! exports provided: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, default */
/***/ (function(module) {

module.exports = JSON.parse("[{\"parameters\":{\"f\":{\"name\":\"f\",\"dtype\":\"FuncType\",\"default\":null}},\"name\":\"AppendOthers\"},{\"parameters\":{},\"name\":\"Component\"},{\"parameters\":{\"average\":{\"name\":\"average\",\"dtype\":\"StrType\",\"default\":null},\"f\":{\"name\":\"f\",\"dtype\":\"FuncType\",\"default\":null}},\"name\":\"InsertAverage\"},{\"parameters\":{\"condition\":{\"name\":\"condition\",\"dtype\":\"IntType\",\"default\":10000}},\"name\":\"ConfirmedConditionFilter\"},{\"parameters\":{},\"name\":\"NanFilter\"},{\"parameters\":{\"f\":{\"name\":\"f\",\"dtype\":\"FuncType\",\"default\":null}},\"name\":\"RecordsFilter\"},{\"parameters\":{\"region\":{\"name\":\"region\",\"dtype\":\"StrType\",\"default\":null}},\"name\":\"RegionFilter\"},{\"parameters\":{\"l\":{\"name\":\"l\",\"dtype\":\"IntType\",\"default\":null}},\"name\":\"SeqFilter\"},{\"parameters\":{\"stage\":{\"name\":\"stage\",\"dtype\":\"StrType\",\"default\":null}},\"name\":\"StageFilter\"},{\"parameters\":{\"daysStartToNow\":{\"name\":\"daysStartToNow\",\"dtype\":\"IntType\",\"default\":7},\"daysEndToNow\":{\"name\":\"daysEndToNow\",\"dtype\":\"IntType\",\"default\":0}},\"name\":\"WeeklyFilter\"},{\"parameters\":{},\"name\":\"Sort\"},{\"parameters\":{},\"name\":\"TopK\"}]");

/***/ }),

/***/ "./dist/sample.json":
/*!**************************!*\
  !*** ./dist/sample.json ***!
  \**************************/
/*! exports provided: name, descriptions, default */
/***/ (function(module) {

module.exports = JSON.parse("{\"name\":\"\",\"descriptions\":[{\"id\":\"weekly_confirmed_data\",\"description\":\"Weekly confirmed data of each country\",\"process\":\"seq\",\"operator\":\"lambda x : [sum(y['新增确诊'] for y in x)]\",\"preprocess\":[{\"name\":\"WeeklyFilter\",\"args\":{\"daysTo\":7}}],\"postprocess\":[{\"name\":\"Sort\"},{\"name\":\"TopK\"},{\"name\":\"AppendOthers\",\"args\":{\"f\":\"lambda x: [sum(y['新增确诊'] for y in x[len(x)-7:])]\"}}]}]}");

/***/ }),

/***/ "./src/interface/component.js":
/*!************************************!*\
  !*** ./src/interface/component.js ***!
  \************************************/
/*! exports provided: ComponentClass, ComponentInstance */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ComponentClass", function() { return ComponentClass; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ComponentInstance", function() { return ComponentInstance; });
/* harmony import */ var _parameter__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./parameter */ "./src/interface/parameter.js");


function ComponentClass(name, parameters){
    this.name = name;
    this.parameters = parameters;
}

function ComponentInstance(componentClass, args){
    this.componentClass = componentClass;
    
    this.args = args;
    if(!this.args){
        this.args = {};
    }
    this.getArg = (pName) => {
        if (pName in this.args){
            return this.args[pName];
        }else{
            return this.componentClass.parameters[pName].defaultValue;
        }
    }
}



/***/ }),

/***/ "./src/interface/description.js":
/*!**************************************!*\
  !*** ./src/interface/description.js ***!
  \**************************************/
/*! exports provided: Description */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Description", function() { return Description; });
function Description(id, info, process, operator, preprocess, postprocess){
    this.id = id;
    this.info = info;
    this.process = process;
    this.operator = operator;
    this.preprocess = preprocess;
    this.postprocess = postprocess;
};


/***/ }),

/***/ "./src/interface/parameter.js":
/*!************************************!*\
  !*** ./src/interface/parameter.js ***!
  \************************************/
/*! exports provided: Parameter */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Parameter", function() { return Parameter; });
function Parameter(dType, defaultValue, name){
    this.dType = dType;
    this.defaultValue = defaultValue;
    this.name = name;
}



/***/ }),

/***/ "./src/main.js":
/*!*********************!*\
  !*** ./src/main.js ***!
  \*********************/
/*! exports provided: Description, ComponentClass, ComponentInstance, Parameter, Parser */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _interface_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./interface/component */ "./src/interface/component.js");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ComponentClass", function() { return _interface_component__WEBPACK_IMPORTED_MODULE_0__["ComponentClass"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ComponentInstance", function() { return _interface_component__WEBPACK_IMPORTED_MODULE_0__["ComponentInstance"]; });

/* harmony import */ var _interface_parameter__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./interface/parameter */ "./src/interface/parameter.js");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Parameter", function() { return _interface_parameter__WEBPACK_IMPORTED_MODULE_1__["Parameter"]; });

/* harmony import */ var _parser_parser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./parser/parser */ "./src/parser/parser.js");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Parser", function() { return _parser_parser__WEBPACK_IMPORTED_MODULE_2__["Parser"]; });

/* harmony import */ var _interface_description__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./interface/description */ "./src/interface/description.js");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Description", function() { return _interface_description__WEBPACK_IMPORTED_MODULE_3__["Description"]; });

/* harmony import */ var _dist_componentClasses_json__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../dist/componentClasses.json */ "./dist/componentClasses.json");
var _dist_componentClasses_json__WEBPACK_IMPORTED_MODULE_4___namespace = /*#__PURE__*/__webpack_require__.t(/*! ../dist/componentClasses.json */ "./dist/componentClasses.json", 1);
/* harmony import */ var _dist_sample_json__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../dist/sample.json */ "./dist/sample.json");
var _dist_sample_json__WEBPACK_IMPORTED_MODULE_5___namespace = /*#__PURE__*/__webpack_require__.t(/*! ../dist/sample.json */ "./dist/sample.json", 1);






// let componentClass = new ComponentClass("test",{});
// console.log(componentClassesJson)
// let parser = new Parser();
// parser.loadComponentClasses(componentClassesJson);
// let description = parser.parseDescription(descriptionsJson.descriptions[0])
// console.log(description);


/***/ }),

/***/ "./src/parser/parser.js":
/*!******************************!*\
  !*** ./src/parser/parser.js ***!
  \******************************/
/*! exports provided: Parser */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Parser", function() { return Parser; });
/* harmony import */ var _interface_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../interface/component */ "./src/interface/component.js");
/* harmony import */ var _interface_parameter__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../interface/parameter */ "./src/interface/parameter.js");
/* harmony import */ var _interface_description__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../interface/description */ "./src/interface/description.js");



function Parser(mode){
    this.mode = mode;
    this.componentClassesLoaded = false;
    this.parseComponentClass = (obj) => {
        let parameters = {};
        for (let key of Object.keys(obj['parameters'])){
            let parameterObj = obj['parameters'][key]
            let parameter = new _interface_parameter__WEBPACK_IMPORTED_MODULE_1__["Parameter"](parameterObj['dtype'], parameterObj['default'], parameterObj['name'])
            parameters[key] = parameter;
        }
        return new _interface_component__WEBPACK_IMPORTED_MODULE_0__["ComponentClass"](obj["name"], parameters);
    };
    this.parseComponentClasses = classes => classes.map(this.parseComponentClass);
    this.loadComponentClasses = classes => {
        let componentClasses = this.parseComponentClasses(classes);
        this.componentClassIndex = {};
        for(let componentClass of componentClasses){
            this.componentClassIndex[componentClass["name"]] = componentClass;
        }
        this.componentClassesLoaded = true;
    }
    this.findComponentClass = (componentClassName) => {
        if (this.componentClassesLoaded){
            return this.componentClassIndex[componentClassName];
        }else{
            if (this.mode === "safe"){
                // Error
            }else{
                // Create a proxy for component class
            }
        }
    }
    this.parseComponentInstance = obj => {
        let componentClass = this.findComponentClass(obj['name'])   
        let args = obj['args']    
        let componentInstance = new _interface_component__WEBPACK_IMPORTED_MODULE_0__["ComponentInstance"](componentClass, args);
        return componentInstance;
    }
    this.parseDescription = obj => {
        let preprocess = obj.preprocess.map(this.parseComponentInstance);
        let postprocess = obj.postprocess.map(this.parseComponentInstance);
        if (! preprocess){
            preprocess = [];
        };
        if(!postprocess){
            postprocess = [];
        }
        return new _interface_description__WEBPACK_IMPORTED_MODULE_2__["Description"](
            obj.id, obj.description, obj.process, obj.operator, preprocess, postprocess
        );
    }

    this.jsonifyComponentInstance = (componentInstance) => {
        return {
            "name": componentInstance.componentClass.name,
            "args": componentInstance.args,
        }
    }
    this.jsonifyDescription = (description) => {
        return {
            "id": description.id,
            "description": description.info,
            "process": description.process,
            "operator": description.operator,
            "preprocess": description.preprocess.map(this.jsonifyComponentInstance),
            "postprocess": description.postprocess.map(this.jsonifyComponentInstance)
        }
    }

}


/***/ })

/******/ });
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9sYW1iZGFEYXRhcHJvY2Vzc0ludGVyZmFjZS93ZWJwYWNrL2Jvb3RzdHJhcCIsIndlYnBhY2s6Ly9sYW1iZGFEYXRhcHJvY2Vzc0ludGVyZmFjZS8uL3NyYy9pbnRlcmZhY2UvY29tcG9uZW50LmpzIiwid2VicGFjazovL2xhbWJkYURhdGFwcm9jZXNzSW50ZXJmYWNlLy4vc3JjL2ludGVyZmFjZS9kZXNjcmlwdGlvbi5qcyIsIndlYnBhY2s6Ly9sYW1iZGFEYXRhcHJvY2Vzc0ludGVyZmFjZS8uL3NyYy9pbnRlcmZhY2UvcGFyYW1ldGVyLmpzIiwid2VicGFjazovL2xhbWJkYURhdGFwcm9jZXNzSW50ZXJmYWNlLy4vc3JjL21haW4uanMiLCJ3ZWJwYWNrOi8vbGFtYmRhRGF0YXByb2Nlc3NJbnRlcmZhY2UvLi9zcmMvcGFyc2VyL3BhcnNlci5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOztRQUFBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTs7UUFFQTtRQUNBOztRQUVBO1FBQ0E7O1FBRUE7UUFDQTtRQUNBOzs7UUFHQTtRQUNBOztRQUVBO1FBQ0E7O1FBRUE7UUFDQTtRQUNBO1FBQ0EsMENBQTBDLGdDQUFnQztRQUMxRTtRQUNBOztRQUVBO1FBQ0E7UUFDQTtRQUNBLHdEQUF3RCxrQkFBa0I7UUFDMUU7UUFDQSxpREFBaUQsY0FBYztRQUMvRDs7UUFFQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0EseUNBQXlDLGlDQUFpQztRQUMxRSxnSEFBZ0gsbUJBQW1CLEVBQUU7UUFDckk7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7UUFDQSwyQkFBMkIsMEJBQTBCLEVBQUU7UUFDdkQsaUNBQWlDLGVBQWU7UUFDaEQ7UUFDQTtRQUNBOztRQUVBO1FBQ0Esc0RBQXNELCtEQUErRDs7UUFFckg7UUFDQTs7O1FBR0E7UUFDQTs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNsRkE7QUFBQTtBQUFBO0FBQUE7QUFBcUM7O0FBRXJDO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7Ozs7Ozs7O0FDckJBO0FBQUE7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7Ozs7Ozs7O0FDUEE7QUFBQTtBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7Ozs7Ozs7O0FDSkE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBdUU7QUFDdkI7QUFDVjtBQUNhO0FBQ2M7QUFDZDtBQUNuRCxvREFBb0Q7QUFDcEQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7Ozs7Ozs7OztBQ1hBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBeUU7QUFDeEI7QUFDSTtBQUNyRDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGdDQUFnQyw4REFBUztBQUN6QztBQUNBO0FBQ0EsbUJBQW1CLG1FQUFjO0FBQ2pDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxvQ0FBb0Msc0VBQWlCO0FBQ3JEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxtQkFBbUIsa0VBQVc7QUFDOUI7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwiZmlsZSI6ImRhdGFwcm9jZXNzLWludGVyZmFjZS5idW5kbGUuanMiLCJzb3VyY2VzQ29udGVudCI6WyIgXHQvLyBUaGUgbW9kdWxlIGNhY2hlXG4gXHR2YXIgaW5zdGFsbGVkTW9kdWxlcyA9IHt9O1xuXG4gXHQvLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuIFx0ZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXG4gXHRcdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuIFx0XHRpZihpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSkge1xuIFx0XHRcdHJldHVybiBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXS5leHBvcnRzO1xuIFx0XHR9XG4gXHRcdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG4gXHRcdHZhciBtb2R1bGUgPSBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSA9IHtcbiBcdFx0XHRpOiBtb2R1bGVJZCxcbiBcdFx0XHRsOiBmYWxzZSxcbiBcdFx0XHRleHBvcnRzOiB7fVxuIFx0XHR9O1xuXG4gXHRcdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuIFx0XHRtb2R1bGVzW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuIFx0XHQvLyBGbGFnIHRoZSBtb2R1bGUgYXMgbG9hZGVkXG4gXHRcdG1vZHVsZS5sID0gdHJ1ZTtcblxuIFx0XHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuIFx0XHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG4gXHR9XG5cblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGVzIG9iamVjdCAoX193ZWJwYWNrX21vZHVsZXNfXylcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubSA9IG1vZHVsZXM7XG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlIGNhY2hlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmMgPSBpbnN0YWxsZWRNb2R1bGVzO1xuXG4gXHQvLyBkZWZpbmUgZ2V0dGVyIGZ1bmN0aW9uIGZvciBoYXJtb255IGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uZCA9IGZ1bmN0aW9uKGV4cG9ydHMsIG5hbWUsIGdldHRlcikge1xuIFx0XHRpZighX193ZWJwYWNrX3JlcXVpcmVfXy5vKGV4cG9ydHMsIG5hbWUpKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIG5hbWUsIHsgZW51bWVyYWJsZTogdHJ1ZSwgZ2V0OiBnZXR0ZXIgfSk7XG4gXHRcdH1cbiBcdH07XG5cbiBcdC8vIGRlZmluZSBfX2VzTW9kdWxlIG9uIGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uciA9IGZ1bmN0aW9uKGV4cG9ydHMpIHtcbiBcdFx0aWYodHlwZW9mIFN5bWJvbCAhPT0gJ3VuZGVmaW5lZCcgJiYgU3ltYm9sLnRvU3RyaW5nVGFnKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFN5bWJvbC50b1N0cmluZ1RhZywgeyB2YWx1ZTogJ01vZHVsZScgfSk7XG4gXHRcdH1cbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsICdfX2VzTW9kdWxlJywgeyB2YWx1ZTogdHJ1ZSB9KTtcbiBcdH07XG5cbiBcdC8vIGNyZWF0ZSBhIGZha2UgbmFtZXNwYWNlIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDE6IHZhbHVlIGlzIGEgbW9kdWxlIGlkLCByZXF1aXJlIGl0XG4gXHQvLyBtb2RlICYgMjogbWVyZ2UgYWxsIHByb3BlcnRpZXMgb2YgdmFsdWUgaW50byB0aGUgbnNcbiBcdC8vIG1vZGUgJiA0OiByZXR1cm4gdmFsdWUgd2hlbiBhbHJlYWR5IG5zIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDh8MTogYmVoYXZlIGxpa2UgcmVxdWlyZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy50ID0gZnVuY3Rpb24odmFsdWUsIG1vZGUpIHtcbiBcdFx0aWYobW9kZSAmIDEpIHZhbHVlID0gX193ZWJwYWNrX3JlcXVpcmVfXyh2YWx1ZSk7XG4gXHRcdGlmKG1vZGUgJiA4KSByZXR1cm4gdmFsdWU7XG4gXHRcdGlmKChtb2RlICYgNCkgJiYgdHlwZW9mIHZhbHVlID09PSAnb2JqZWN0JyAmJiB2YWx1ZSAmJiB2YWx1ZS5fX2VzTW9kdWxlKSByZXR1cm4gdmFsdWU7XG4gXHRcdHZhciBucyA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18ucihucyk7XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShucywgJ2RlZmF1bHQnLCB7IGVudW1lcmFibGU6IHRydWUsIHZhbHVlOiB2YWx1ZSB9KTtcbiBcdFx0aWYobW9kZSAmIDIgJiYgdHlwZW9mIHZhbHVlICE9ICdzdHJpbmcnKSBmb3IodmFyIGtleSBpbiB2YWx1ZSkgX193ZWJwYWNrX3JlcXVpcmVfXy5kKG5zLCBrZXksIGZ1bmN0aW9uKGtleSkgeyByZXR1cm4gdmFsdWVba2V5XTsgfS5iaW5kKG51bGwsIGtleSkpO1xuIFx0XHRyZXR1cm4gbnM7XG4gXHR9O1xuXG4gXHQvLyBnZXREZWZhdWx0RXhwb3J0IGZ1bmN0aW9uIGZvciBjb21wYXRpYmlsaXR5IHdpdGggbm9uLWhhcm1vbnkgbW9kdWxlc1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5uID0gZnVuY3Rpb24obW9kdWxlKSB7XG4gXHRcdHZhciBnZXR0ZXIgPSBtb2R1bGUgJiYgbW9kdWxlLl9fZXNNb2R1bGUgP1xuIFx0XHRcdGZ1bmN0aW9uIGdldERlZmF1bHQoKSB7IHJldHVybiBtb2R1bGVbJ2RlZmF1bHQnXTsgfSA6XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0TW9kdWxlRXhwb3J0cygpIHsgcmV0dXJuIG1vZHVsZTsgfTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kKGdldHRlciwgJ2EnLCBnZXR0ZXIpO1xuIFx0XHRyZXR1cm4gZ2V0dGVyO1xuIFx0fTtcblxuIFx0Ly8gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm8gPSBmdW5jdGlvbihvYmplY3QsIHByb3BlcnR5KSB7IHJldHVybiBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwob2JqZWN0LCBwcm9wZXJ0eSk7IH07XG5cbiBcdC8vIF9fd2VicGFja19wdWJsaWNfcGF0aF9fXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnAgPSBcIlwiO1xuXG5cbiBcdC8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuIFx0cmV0dXJuIF9fd2VicGFja19yZXF1aXJlX18oX193ZWJwYWNrX3JlcXVpcmVfXy5zID0gXCIuL3NyYy9tYWluLmpzXCIpO1xuIiwiaW1wb3J0IHtQYXJhbWV0ZXJ9IGZyb20gXCIuL3BhcmFtZXRlclwiXG5cbmZ1bmN0aW9uIENvbXBvbmVudENsYXNzKG5hbWUsIHBhcmFtZXRlcnMpe1xuICAgIHRoaXMubmFtZSA9IG5hbWU7XG4gICAgdGhpcy5wYXJhbWV0ZXJzID0gcGFyYW1ldGVycztcbn1cblxuZnVuY3Rpb24gQ29tcG9uZW50SW5zdGFuY2UoY29tcG9uZW50Q2xhc3MsIGFyZ3Mpe1xuICAgIHRoaXMuY29tcG9uZW50Q2xhc3MgPSBjb21wb25lbnRDbGFzcztcbiAgICBcbiAgICB0aGlzLmFyZ3MgPSBhcmdzO1xuICAgIGlmKCF0aGlzLmFyZ3Mpe1xuICAgICAgICB0aGlzLmFyZ3MgPSB7fTtcbiAgICB9XG4gICAgdGhpcy5nZXRBcmcgPSAocE5hbWUpID0+IHtcbiAgICAgICAgaWYgKHBOYW1lIGluIHRoaXMuYXJncyl7XG4gICAgICAgICAgICByZXR1cm4gdGhpcy5hcmdzW3BOYW1lXTtcbiAgICAgICAgfWVsc2V7XG4gICAgICAgICAgICByZXR1cm4gdGhpcy5jb21wb25lbnRDbGFzcy5wYXJhbWV0ZXJzW3BOYW1lXS5kZWZhdWx0VmFsdWU7XG4gICAgICAgIH1cbiAgICB9XG59XG5cbmV4cG9ydCB7Q29tcG9uZW50Q2xhc3MsIENvbXBvbmVudEluc3RhbmNlfSIsImZ1bmN0aW9uIERlc2NyaXB0aW9uKGlkLCBpbmZvLCBwcm9jZXNzLCBvcGVyYXRvciwgcHJlcHJvY2VzcywgcG9zdHByb2Nlc3Mpe1xuICAgIHRoaXMuaWQgPSBpZDtcbiAgICB0aGlzLmluZm8gPSBpbmZvO1xuICAgIHRoaXMucHJvY2VzcyA9IHByb2Nlc3M7XG4gICAgdGhpcy5vcGVyYXRvciA9IG9wZXJhdG9yO1xuICAgIHRoaXMucHJlcHJvY2VzcyA9IHByZXByb2Nlc3M7XG4gICAgdGhpcy5wb3N0cHJvY2VzcyA9IHBvc3Rwcm9jZXNzO1xufTtcbmV4cG9ydCB7RGVzY3JpcHRpb259OyIsImZ1bmN0aW9uIFBhcmFtZXRlcihkVHlwZSwgZGVmYXVsdFZhbHVlLCBuYW1lKXtcbiAgICB0aGlzLmRUeXBlID0gZFR5cGU7XG4gICAgdGhpcy5kZWZhdWx0VmFsdWUgPSBkZWZhdWx0VmFsdWU7XG4gICAgdGhpcy5uYW1lID0gbmFtZTtcbn1cblxuZXhwb3J0IHtQYXJhbWV0ZXJ9IiwiaW1wb3J0IHtDb21wb25lbnRDbGFzcywgQ29tcG9uZW50SW5zdGFuY2V9IGZyb20gXCIuL2ludGVyZmFjZS9jb21wb25lbnRcIlxuaW1wb3J0IHtQYXJhbWV0ZXJ9IGZyb20gXCIuL2ludGVyZmFjZS9wYXJhbWV0ZXJcIjtcbmltcG9ydCB7UGFyc2VyfSBmcm9tIFwiLi9wYXJzZXIvcGFyc2VyXCJcbmltcG9ydCB7RGVzY3JpcHRpb259IGZyb20gXCIuL2ludGVyZmFjZS9kZXNjcmlwdGlvblwiXG5pbXBvcnQgY29tcG9uZW50Q2xhc3Nlc0pzb24gZnJvbSBcIi4uL2Rpc3QvY29tcG9uZW50Q2xhc3Nlcy5qc29uXCI7XG5pbXBvcnQgZGVzY3JpcHRpb25zSnNvbiBmcm9tIFwiLi4vZGlzdC9zYW1wbGUuanNvblwiO1xuLy8gbGV0IGNvbXBvbmVudENsYXNzID0gbmV3IENvbXBvbmVudENsYXNzKFwidGVzdFwiLHt9KTtcbi8vIGNvbnNvbGUubG9nKGNvbXBvbmVudENsYXNzZXNKc29uKVxuLy8gbGV0IHBhcnNlciA9IG5ldyBQYXJzZXIoKTtcbi8vIHBhcnNlci5sb2FkQ29tcG9uZW50Q2xhc3Nlcyhjb21wb25lbnRDbGFzc2VzSnNvbik7XG4vLyBsZXQgZGVzY3JpcHRpb24gPSBwYXJzZXIucGFyc2VEZXNjcmlwdGlvbihkZXNjcmlwdGlvbnNKc29uLmRlc2NyaXB0aW9uc1swXSlcbi8vIGNvbnNvbGUubG9nKGRlc2NyaXB0aW9uKTtcbmV4cG9ydCB7XG4gICAgRGVzY3JpcHRpb24sIENvbXBvbmVudENsYXNzLCBDb21wb25lbnRJbnN0YW5jZSwgUGFyYW1ldGVyLCBQYXJzZXJcbn0iLCJpbXBvcnQge0NvbXBvbmVudENsYXNzLCBDb21wb25lbnRJbnN0YW5jZX0gZnJvbSBcIi4uL2ludGVyZmFjZS9jb21wb25lbnRcIjtcbmltcG9ydCB7UGFyYW1ldGVyfSBmcm9tIFwiLi4vaW50ZXJmYWNlL3BhcmFtZXRlclwiO1xuaW1wb3J0IHtEZXNjcmlwdGlvbn0gZnJvbSBcIi4uL2ludGVyZmFjZS9kZXNjcmlwdGlvblwiO1xuZnVuY3Rpb24gUGFyc2VyKG1vZGUpe1xuICAgIHRoaXMubW9kZSA9IG1vZGU7XG4gICAgdGhpcy5jb21wb25lbnRDbGFzc2VzTG9hZGVkID0gZmFsc2U7XG4gICAgdGhpcy5wYXJzZUNvbXBvbmVudENsYXNzID0gKG9iaikgPT4ge1xuICAgICAgICBsZXQgcGFyYW1ldGVycyA9IHt9O1xuICAgICAgICBmb3IgKGxldCBrZXkgb2YgT2JqZWN0LmtleXMob2JqWydwYXJhbWV0ZXJzJ10pKXtcbiAgICAgICAgICAgIGxldCBwYXJhbWV0ZXJPYmogPSBvYmpbJ3BhcmFtZXRlcnMnXVtrZXldXG4gICAgICAgICAgICBsZXQgcGFyYW1ldGVyID0gbmV3IFBhcmFtZXRlcihwYXJhbWV0ZXJPYmpbJ2R0eXBlJ10sIHBhcmFtZXRlck9ialsnZGVmYXVsdCddLCBwYXJhbWV0ZXJPYmpbJ25hbWUnXSlcbiAgICAgICAgICAgIHBhcmFtZXRlcnNba2V5XSA9IHBhcmFtZXRlcjtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gbmV3IENvbXBvbmVudENsYXNzKG9ialtcIm5hbWVcIl0sIHBhcmFtZXRlcnMpO1xuICAgIH07XG4gICAgdGhpcy5wYXJzZUNvbXBvbmVudENsYXNzZXMgPSBjbGFzc2VzID0+IGNsYXNzZXMubWFwKHRoaXMucGFyc2VDb21wb25lbnRDbGFzcyk7XG4gICAgdGhpcy5sb2FkQ29tcG9uZW50Q2xhc3NlcyA9IGNsYXNzZXMgPT4ge1xuICAgICAgICBsZXQgY29tcG9uZW50Q2xhc3NlcyA9IHRoaXMucGFyc2VDb21wb25lbnRDbGFzc2VzKGNsYXNzZXMpO1xuICAgICAgICB0aGlzLmNvbXBvbmVudENsYXNzSW5kZXggPSB7fTtcbiAgICAgICAgZm9yKGxldCBjb21wb25lbnRDbGFzcyBvZiBjb21wb25lbnRDbGFzc2VzKXtcbiAgICAgICAgICAgIHRoaXMuY29tcG9uZW50Q2xhc3NJbmRleFtjb21wb25lbnRDbGFzc1tcIm5hbWVcIl1dID0gY29tcG9uZW50Q2xhc3M7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5jb21wb25lbnRDbGFzc2VzTG9hZGVkID0gdHJ1ZTtcbiAgICB9XG4gICAgdGhpcy5maW5kQ29tcG9uZW50Q2xhc3MgPSAoY29tcG9uZW50Q2xhc3NOYW1lKSA9PiB7XG4gICAgICAgIGlmICh0aGlzLmNvbXBvbmVudENsYXNzZXNMb2FkZWQpe1xuICAgICAgICAgICAgcmV0dXJuIHRoaXMuY29tcG9uZW50Q2xhc3NJbmRleFtjb21wb25lbnRDbGFzc05hbWVdO1xuICAgICAgICB9ZWxzZXtcbiAgICAgICAgICAgIGlmICh0aGlzLm1vZGUgPT09IFwic2FmZVwiKXtcbiAgICAgICAgICAgICAgICAvLyBFcnJvclxuICAgICAgICAgICAgfWVsc2V7XG4gICAgICAgICAgICAgICAgLy8gQ3JlYXRlIGEgcHJveHkgZm9yIGNvbXBvbmVudCBjbGFzc1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuICAgIHRoaXMucGFyc2VDb21wb25lbnRJbnN0YW5jZSA9IG9iaiA9PiB7XG4gICAgICAgIGxldCBjb21wb25lbnRDbGFzcyA9IHRoaXMuZmluZENvbXBvbmVudENsYXNzKG9ialsnbmFtZSddKSAgIFxuICAgICAgICBsZXQgYXJncyA9IG9ialsnYXJncyddICAgIFxuICAgICAgICBsZXQgY29tcG9uZW50SW5zdGFuY2UgPSBuZXcgQ29tcG9uZW50SW5zdGFuY2UoY29tcG9uZW50Q2xhc3MsIGFyZ3MpO1xuICAgICAgICByZXR1cm4gY29tcG9uZW50SW5zdGFuY2U7XG4gICAgfVxuICAgIHRoaXMucGFyc2VEZXNjcmlwdGlvbiA9IG9iaiA9PiB7XG4gICAgICAgIGxldCBwcmVwcm9jZXNzID0gb2JqLnByZXByb2Nlc3MubWFwKHRoaXMucGFyc2VDb21wb25lbnRJbnN0YW5jZSk7XG4gICAgICAgIGxldCBwb3N0cHJvY2VzcyA9IG9iai5wb3N0cHJvY2Vzcy5tYXAodGhpcy5wYXJzZUNvbXBvbmVudEluc3RhbmNlKTtcbiAgICAgICAgaWYgKCEgcHJlcHJvY2Vzcyl7XG4gICAgICAgICAgICBwcmVwcm9jZXNzID0gW107XG4gICAgICAgIH07XG4gICAgICAgIGlmKCFwb3N0cHJvY2Vzcyl7XG4gICAgICAgICAgICBwb3N0cHJvY2VzcyA9IFtdO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBuZXcgRGVzY3JpcHRpb24oXG4gICAgICAgICAgICBvYmouaWQsIG9iai5kZXNjcmlwdGlvbiwgb2JqLnByb2Nlc3MsIG9iai5vcGVyYXRvciwgcHJlcHJvY2VzcywgcG9zdHByb2Nlc3NcbiAgICAgICAgKTtcbiAgICB9XG5cbiAgICB0aGlzLmpzb25pZnlDb21wb25lbnRJbnN0YW5jZSA9IChjb21wb25lbnRJbnN0YW5jZSkgPT4ge1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgXCJuYW1lXCI6IGNvbXBvbmVudEluc3RhbmNlLmNvbXBvbmVudENsYXNzLm5hbWUsXG4gICAgICAgICAgICBcImFyZ3NcIjogY29tcG9uZW50SW5zdGFuY2UuYXJncyxcbiAgICAgICAgfVxuICAgIH1cbiAgICB0aGlzLmpzb25pZnlEZXNjcmlwdGlvbiA9IChkZXNjcmlwdGlvbikgPT4ge1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgXCJpZFwiOiBkZXNjcmlwdGlvbi5pZCxcbiAgICAgICAgICAgIFwiZGVzY3JpcHRpb25cIjogZGVzY3JpcHRpb24uaW5mbyxcbiAgICAgICAgICAgIFwicHJvY2Vzc1wiOiBkZXNjcmlwdGlvbi5wcm9jZXNzLFxuICAgICAgICAgICAgXCJvcGVyYXRvclwiOiBkZXNjcmlwdGlvbi5vcGVyYXRvcixcbiAgICAgICAgICAgIFwicHJlcHJvY2Vzc1wiOiBkZXNjcmlwdGlvbi5wcmVwcm9jZXNzLm1hcCh0aGlzLmpzb25pZnlDb21wb25lbnRJbnN0YW5jZSksXG4gICAgICAgICAgICBcInBvc3Rwcm9jZXNzXCI6IGRlc2NyaXB0aW9uLnBvc3Rwcm9jZXNzLm1hcCh0aGlzLmpzb25pZnlDb21wb25lbnRJbnN0YW5jZSlcbiAgICAgICAgfVxuICAgIH1cblxufVxuZXhwb3J0IHtQYXJzZXJ9Il0sInNvdXJjZVJvb3QiOiIifQ==