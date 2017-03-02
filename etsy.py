'''
Author: Michael Harris https://github.com/Harris-Mike
Date: 10/10/2015

This is a bot for the site etsy.com

User supplies a text file with login name, password, and store URL along with a number of times purchase needs to be made

Reades info from text, injects into webpage

in loop:
Tries to find element of page, if cannot find throw webdriver "NoSuchElementException" and refresh page

to break out of loop element must exist

routes to item page, clicks buy now and is redirected to submit order which clicks sumbit and order is made

for each successful order add 1 to successfol_purchase_counter

repeat loop until # of successful purchases equals second argsparse command
'''



import parser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import argparse
import time
import sys
#import easygui



def main(log_file,counter):

    #reads text file for future use
    log_file_list=[]
    file = open(log_file,'r')
    for line in file:
        log_file_list.append(line.strip())

    username_input=log_file_list[0]
    password_input=log_file_list[1]
    store_input=log_file_list[2]

    #ask for item name being searched
    item_name=input("Please enter item name you wish to purchase (surrounded by quotes) \n")
    print("Starting webdriver....")
    driver = webdriver.Remote(desired_capabilities={'browserName': 'htmlunit', "applicationCacheEnabled" : False, 'javascriptEnabled': False, 'platform': 'ANY', 'version': '', 'setThrowExceptionOnScriptError': False})
    print("Webdriver successfully started.")
    start_time=time.clock()


    #open etsy, click sign in button, insert username and password and submit

    driver.get("https://www.etsy.com/signin")

    # login
    print("Attempting to sign in...")
    username_input_form=driver.find_element_by_id("username-existing")
    username_input_form.send_keys(username_input)
    password_input_form=driver.find_element_by_id('password-existing')
    password_input_form.send_keys(password_input)
    sign_in_button=driver.find_element_by_xpath('//*[@id="signin_button"]')
    sign_in_button.click()
    if driver.current_url=="https://www.etsy.com/signin":
        sys.exit("Invalid login info.  Please adjust .txt for valid login info")

    # reroute to store
    print("Sign in Successful")
    driver.get(store_input)
    print("Redirecting to store....")


    #Search for item on page, if found click, if not found catch exception and refresh
    successful_purchase_counter=0
    while successful_purchase_counter<counter:
        on_page=False
        while(on_page==False):
            try:
                print("Searching....")
                sale_item=driver.find_element_by_xpath("//a[contains(.,'" + item_name + "')]")
                print("Store is updated. \n'" + item_name + "' on page. \nRedirecting....")
                on_page=True
            except NoSuchElementException:
                print("not found....refreshing....")
                driver.sleep(5000)
                driver.get(store_input)
        sale_item.click()


        # click buy now button, if sold out catch exception buy it now does not exist, break

        try:
            buy_now_button=driver.find_element_by_xpath("//button[contains(.,'Buy It Now')]")
        except NoSuchElementException:
            print("item sold out....going back to shop page")
            driver.get(store_input)
            continue
        print("Clicking 'Buy It Now'....")
        buy_now_button.click()
        #buy page
        try:
            submit_order_button = driver.find_element_by_xpath("//button[contains(., 'Submit Order')]")
        except NoSuchElementException:
            print("item sold out....going back to shop page")
            driver.get(store_input)
            continue
        submit_order_button.click()
        print("Submitting order....")


        # #time test
        # # end_time=time.clock()
        # # print("it took " ,end_time, '-',start_time,'=',(time.clock()-start_time) , "seconds to reach this page")
        # # input()
        #
        successful_purchase_counter=successful_purchase_counter+1
        print('Item successfully purchased!  Bought' + successful_purchase_counter + ' of ' + str(counter))
        driver.get(store_input) #redirect to store to complete loop
    print("Program has successfully completed the user entered input of: " +str(counter))
    print("Quitting........")

parser = argparse.ArgumentParser()
parser.add_argument('file', help="A text file with three lines: username, password, store URL")
parser.add_argument('counter', type=int, help="how many successful purchases you want")
args=parser.parse_args()
main(args.file,args.counter)
