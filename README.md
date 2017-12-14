# xlr-selenium-plugin

[![Build Status](https://travis-ci.org/xebialabs-community/xlr-selenium-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-selenium-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b19a0cb98fba4b9cb7b6a17b67dbd4eb)](https://www.codacy.com/app/xebialabs-community/xlr-selenium-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-selenium-plugin&amp;utm_campaign=Badge_Grade)
[![Code Climate](https://codeclimate.com/github/xebialabs-community/xlr-selenium-plugin/badges/gpa.svg)](https://codeclimate.com/github/xebialabs-community/xlr-selenium-plugin)
[![License: MIT][xlr-selenium-plugin-license-image]][xlr-selenium-plugin-license-url]
[![Github All Releases][xlr-selenium-plugin-downloads-image]]()

[xlr-selenium-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-selenium-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-selenium-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-selenium-plugin/total.svg

# XL Release Selenium Plugin

## Preface
This document describes the functionality provide by the `xlr-selenium-plugin`

## Overview
This module offers a basic interface to Selenium functionality.

## Installation
1. Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.

2. The Selenium plugin requires XL Release to be able to use the [Python language bindings for Selenium WebDriver](https://github.com/SeleniumHQ/selenium/tree/master/py).  Once you have downloaded Selenium WebDriver, you must add the python classes to the <XL_RELEASE>/lib/jython-standalone-2.7.0.jar by running the following command:

`zip -u -r jython-standalone-2.7.0.jar Lib/*`
## Available Tasks

### Create Selenium task type

The **Selenium: Execute Test Script** task type runs Selenium test scripts. It requires you to specify the following information:

* URL for WebDriver Hub 
* The web browser that you want to test with

![XL Release Selenium Task](images/selenium-task.png)

Additionally, for testing with Selenium Test Suites, you can specify:

* Starting URL
* Location of Test Suite Files
* Integer representing a threshold for failed test cases

## XL Release Scenario

Selenium is a framework that allow automated testing through a browser. Selenium however is not 'one standard thing'. There's Selenium IDE, Selenium WebDriver, Selenium Grid... there a plethora of ways to run, orchestrate and process test results. Therefore this plugin is focused on a narrow use case: simple smoketest that are specified inline the testcase or in a python script in GIT with a simple zero or one return code.

### Design decisions on plugin scope

1. The 'what'. The test cases, which contain code to interact with browsers, execute actions, verify behavior, etcetera. The test cases can be specified in a different languages like Java, C#, Python, NodeJS, HTML that have language bindings to Selenium available. Essentially, test cases are as custom as the application code test test: they are no 'standard formats' to speak of. Also, all these testruns can result in various form of output: a simple return code (suitable for smoke tests), a HTML report (suitable for archiving as future reference) and xUnit test results. So sadly, there's no 'standard' selenium test case output either. These testcases are (potentially) grouped in a suite. Suites specify order, parallelism and hints on which browsers to use. Popular frameworks to run testcases are JUnit, TestNG and nUnit. Essentially this means that for each of these variants the plugin should have a task: something that is a large effort to build and maintain. Therefore we support only python-based selenium scripts.

1. The 'where'. A WebDriver daemon take care of communicating with the various browsers on various operation system. This usually a server-side (remote) piece where the Selenium connects to using TCP. This "Remote WebDriver" that allows the aforementioned code to drive browsers remotely. There are various 'products' that implement the WebDriver API that can take care of cross-browser tests, parallelism, queueing etc. Selenium Hub and Grid are quite a bit of work to be set up, see for example [here](http://www.tothenew.com/blog/parallel-execution-with-selenium-grid/). This plugin allows you to configure various endpoints that will be passed to the running tests. Sadly, there is no standard way to inject that configuration in the Selenium client, which means we'll require the selenium scripts to use the XLR-specific factory to obtain a WebDriver instance.

Customers generally invoke Selenium testing during the Continuous Integration phase of building code, using their CI tool to run Selenium testing for Developers to validate their code changes.

These same Selenium tests can be run in different environments.  A sample XL Release template shows how QA can leverage the automated Selenium tests as part of their overall testing effort 

![XL Release Template using Selenium Testing in Parallel test group](images/selenium-testing-example.png)
--- 

## References:
* [Selenium WebDriver](http://www.seleniumhq.org/projects/webdriver/)
