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

## XL Release Scenario

Selenium is a framework that allow automated testing driving a browser. Selenium however is not 'one standard thing'. There's Selenium IDE, Selenium WebDriver, Selenium Grid... there a plethora of ways to run, orchestrate and process test results. Therefore this plugin is focused on a narrow use case: simple smoketest that are specified inline the XLR task.

### Design decisions on plugin scope

1. The 'what'. The test cases, which contain code to interact with browsers, execute actions, verify behavior, etcetera. The test cases can be specified in a different languages like Java, C#, Python, NodeJS, HTML that have language bindings to Selenium available. Essentially, test cases are as custom as the application code they test: there are no 'standard formats' to speak of. Also, all these testruns can result in various form of outputs: a simple return code (suitable for smoke tests), a HTML report (suitable for archiving as future reference) and xUnit test results (suitable to parse and make automated decision on pass/fail). So sadly, there's no 'standard' selenium test case output either. These testcases are (potentially) grouped in a suite. Suites specify order, parallelism and hints on which browsers to use. Popular frameworks to run testcases are JUnit, TestNG and nUnit. Essentially this means that for each of these variants the plugin should have a separate task: something that is a large effort to build and maintain. Therefore this plugins supports only python-based selenium scripts.

1. The 'where'. A WebDriver daemon takes care of communicating with the various browsers on various operation system. This usually a server-side (remote) piece where the Selenium connects to using TCP. This "Remote WebDriver" that allows the aforementioned code to drive browsers remotely. There are various 'products' that implement the WebDriver API that can take care of cross-browser tests, parallelism, queueing etc. Selenium Hub and Grid are quite a bit of work to be set up, see for example [here](http://www.tothenew.com/blog/parallel-execution-with-selenium-grid/). This plugin ships with an example docker configuration that allows you to run tests on a hub connected to two docker containers running firefox and chrome. This plugin allows you to configure various endpoints that will be passed to the running tests. Sadly, there is no standard way to inject that configuration in the Selenium client, which means we'll require the selenium scripts to use the XLR-specific convention to interact with a WebDriver instance.

## Installation
1. Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.
2. Configure your Remote Web Driver / WebDriver / Grid in Shared Configuration

## Available Tasks

### Create Selenium Test Case

The **Selenium: Run Python Test Case** task type runs Selenium test scripts specified in the Python language. It requires you to specify the following information:

* Selenium Profile (include grid URL, desired capabilities and optionally another host that the XLR server to run the python on)
* The test case you want to run as inline Python. The WebDriver object ```driver``` will be made available to the test script, and it will execute ```driver.quit()``` as a post test action.


## Testing this plugin

1. Run the build.sh in the ```python-selenium-docker-image```
2. Run ```./gradlew runDockerCompose```

## References:
* [Selenium WebDriver](http://www.seleniumhq.org/projects/webdriver/)
