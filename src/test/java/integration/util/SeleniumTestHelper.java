/**
 * Copyright 2020 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package integration.util;

import static io.restassured.RestAssured.baseURI;
import static io.restassured.RestAssured.given;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

import com.google.common.collect.Maps;
import java.util.Scanner;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

public final class SeleniumTestHelper {

    private static final String BASE_URI = "http://localhost:15516/api/v1";
    private static RequestSpecification httpRequest = null;
    private static final String IMPORT_CONFIG = "/config";
    private static final String IMPORT_TEMPLATE = "/templates/import";
    private static final String START_RELEASE_SELENIUM = "/templates/Applications/Release832b197247d146298a22732556c67e80/start";
    private static final String GET_RELEASE_PREFIX = "/releases/";
    private static final String GET_VARIABLES_SUFFIX = "/variableValues";
    
    private SeleniumTestHelper() {
        /*
         * Private Constructor will prevent the instantiation of this class directly
         */
    }

    static {
        baseURI = BASE_URI;
        // Configure authentication
        httpRequest = given().auth().preemptive().basic("admin", "admin");
    }

    public static void initializeXLR() throws InterruptedException{
        System.out.println("Pausing for 1.5 minutes, waiting for XLR to start. ");
        Thread.sleep(90000);

        // Load server config for the python/selenium server where scripts are run
        try {
            // Load config
            JSONObject requestParamsConfig = getRequestParamsFromFile(getResourceFilePath("docker/initialize/data/server-configs.json"));
            httpRequest.header("Content-Type", "application/json");
            httpRequest.header("Accept", "application/json");
            httpRequest.body(requestParamsConfig.toJSONString());
            
            // Post server config
            Response response = httpRequest.post(IMPORT_CONFIG);
            if (response.getStatusCode() != 200) {
                System.out.println("Status line, import server was " + response.getStatusLine() + "");
            } else {
                //String responseId = response.jsonPath().getString("id");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        try {
            // Load the template
            JSONObject requestParams = new JSONObject();
            httpRequest.body(requestParams.toJSONString());
            httpRequest.contentType("multipart/form-data");
            httpRequest.multiPart(new File(getResourceFilePath("docker/initialize/data/release-template-selenium.json")));
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        // Post template
        Response response = httpRequest.post(IMPORT_TEMPLATE);
        if (response.getStatusCode() != 200) {
            System.out.println("Status line, import template was " + response.getStatusLine() + "");
        } else {
            String postResponseId = response.jsonPath().getString("id");
        }
    }

    public static String getSeleniumReleaseResult() throws InterruptedException{
        org.json.JSONObject releaseResultJSON = null;
        String responseId = "";
        String releaseResultStr = "";
        // Prepare httpRequest, start the release
        JSONObject requestParams = getRequestParams();
        Response response = given().auth().preemptive().basic("admin", "admin")
            .header("Content-Type", "application/json")
            .header("Accept", "application/json")
            .body(requestParams.toJSONString())
            .post(START_RELEASE_SELENIUM);

        ///////// retrieve the planned release id.
        if (response.getStatusCode() != 200) {
            System.out.println("Status line, Start release was " + response.getStatusLine() );
        } else {
            responseId = response.jsonPath().getString("id");
            System.out.println("Start release was successful, id = "+ responseId);
        }

        ///////// Get Archived responses
        // Sleep so XLR can finish processing releases
        System.out.println("Pausing for 2 minutes, waiting for release to complete. If most requests fail with 404, consider sleeping longer.");
        Thread.sleep(120000);
        //////////
        response = given().auth().preemptive().basic("admin", "admin")
        .header("Content-Type", "application/json")
        .header("Accept", "application/json")
        .body(requestParams.toJSONString())
        .get(GET_RELEASE_PREFIX + responseId + GET_VARIABLES_SUFFIX);

        if (response.getStatusCode() != 200) {
            System.out.println("Status line for get variables was " + response.getStatusLine() + "");
        } else {
            //releaseResult = response.jsonPath().get("phases[0].tasks[1].comments[0].text").toString();
            releaseResultStr = response.jsonPath().prettyPrint();    
        }
        // Return the comments attached to the finished release so we can test for success
        return releaseResultStr;
    }

    /////////////////// Util methods

    public static String getResourceFilePath(String filePath){ 
        // Working with resource files instead of the file system - OS Agnostic 
        String resourcePath = "";
        ClassLoader classLoader = SeleniumTestHelper.class.getClassLoader();
        try {
            resourcePath = new File (classLoader.getResource(filePath).toURI()).getAbsolutePath();
        } catch (Exception e) {
            e.printStackTrace();
        }
        //System.out.println("resourcePath = " + resourcePath);
        return resourcePath;
    }

    public static String readFile(String path) {
        StringBuilder result = new StringBuilder("");

        File file = new File(path);
        try (Scanner scanner = new Scanner(file)) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                result.append(line).append("\n");
            }
            scanner.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result.toString();
    }

    public static JSONObject getRequestParamsFromFile(String filePath) {
        JSONObject requestParams = new JSONObject();

        //JSON parser object to parse read file
        JSONParser jsonParser = new JSONParser();
         
        try (FileReader reader = new FileReader(filePath))
        {
            //Read JSON file
            Object obj = jsonParser.parse(reader);
 
            requestParams = (JSONObject) obj;
            //System.out.println(requestParams);
 
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return requestParams;
    }

    public static JSONObject getRequestParams() {
        // must use intermediate parameterized HashMap to avoid warnings
        HashMap<String,Object> params = new HashMap<String,Object>();
        
        params.put("releaseTitle", "release from api");
        //params.put("variables", new JSONObject());
        //params.put("releaseVariables", new JSONObject());
        //params.put("releasePasswordVariables", new JSONObject());
        //params.put("scheduledStartDate", null);
        //params.put("autoStart", false);
        JSONObject requestParams = new JSONObject(params);
        return requestParams;
    }

}