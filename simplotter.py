# -*- coding: utf-8 -*-
"""
Plot data produced during Trust Model simulations

Created on Sat Oct 13 18:33 2018

@author: Cara Lynch
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import math

def read_olddata(infile):
    """
    Reads files and puts data into arrays
    
    :param infile: string, name of file to read
    :return array: numpy array of all data from file
    """
    with open(infile, "rt") as file:
        
        lines = file.readlines()
        width = len(lines[0].split(','))
        length = len(lines)
        
        array = np.zeros((length,width))
        
        for i in range(0, len(lines)):
            linetokens = lines[i].split(',')
            for n in range(0, len(linetokens)):
                array[i,n] = float(linetokens[n])
        return array
        
def read_newdata(infile):
    """
    Reads files and puts data into arrays.
    The files would have the timesteps in the first column and the retailer indices in the first row
    
    :param infile: string name of file to read
    :return timesteps: numpy array of timesteps 
    :return data: numpy array of data
    """
    with open(infile, "rt") as Infile:
        
        lines = Infile.readlines()
        width = len(lines[1].split(',')) - 1
        length = len(lines) - 1
        
        data = np.zeros((length,width))
        timesteps = np.zeros(length)
        
        for i in range(1, length+1):
            linetokens = lines[i].split(',')
            timesteps[i-1] = linetokens[0]
            for n in range(1, len(linetokens)):
                data[i-1,n-1] = float(linetokens[n])
        return timesteps, data

## get data for all runs

def get_data(gossip_mode):
    """
    Gets data from  files for all runs in directory
    
    :param gossip_mode: string indicating which gossip mode is used
    :param new_or_old: string indicating whether the output files are in new or old format
    :return retailer_data: list of lists, each run is one element, each element is a list of
    numpy arrays (directory, timesteps, inventory, price, quality, trust in retailer, quality/price and gossip trust if friendly mode)
    :return supplier_data: list of lists, each run is an element, each element a list of numpy arrays
    (directory, timesteps, inventory, quality, quality/price and trust if applicable)
    :return retailer_mean_data: list of lists, each run is an element, each element a list of numpy arrays
    (directory, timesteps, mean prices and stdevs, mean quality and stdevs, mean trust and stdevs, mean q/p and stdevs, mean gossip trust and stdevs)
    :param supplier_mean_data: list of lists, each run is an element, each element a list of numpy array
    (directory, timesteps, mean prices and stdevs, mean quality and stdevs, mean q/p and stdevs, mean trust and stdevs)
    """
    
    ## create empty lists for data from each run
    retailer_data = []
    retailer_mean_data = []
    supplier_data = []
    supplier_mean_data = []
    
    for directory in os.listdir("."):
        if os.path.isdir(directory):
            if os.path.exists(directory + "/RetailerInventories.csv"):

                    
                timesteps, retailer_inventory = read_newdata(directory+"/RetailerInventories.csv")
                timesteps, retailer_price = read_newdata(directory+"/RetailerPrices.csv")
                timesteps, retailer_quality = read_newdata(directory + "/RetailerQualities.csv")
                
                timesteps,supplier_inventory = read_newdata(directory+"/SupplierInventories.csv")
                timesteps,supplier_price = read_newdata(directory+"/SupplierPrices.csv")
                timesteps,supplier_quality = read_newdata(directory + "/SupplierQualities.csv")
                
                timesteps, retailer_trust = read_newdata(directory + "/TrustInRetailers.csv")
                timesteps, supplier_trust = read_newdata(directory + "/TrustInSuppliers.csv")
                
                if gossip_mode == "f":
                    timesteps, gossip_trust = read_newdata(directory + "/GossipTrust.csv")
                        
                        
                # interesting calculations
                retailer_quality_price = np.divide(retailer_quality, retailer_price)
                supplier_quality_price = np.divide(supplier_quality, supplier_price)
                
                # add data to list for this run
                retailer_run_list = [directory, timesteps, retailer_inventory, retailer_price, retailer_quality, retailer_trust, retailer_quality_price]
                if gossip_mode == "f":
                    retailer_run_list.append(gossip_trust)
                supplier_run_list = [directory, timesteps, supplier_inventory, supplier_price, supplier_quality, supplier_quality_price]
                supplier_run_list.append(supplier_trust)
                
                
                # get mean values and standard deviations over all retailers and suppliers
                retailer_price_mean_std = np.zeros((np.ma.size(timesteps),2))
                retailer_quality_mean_std = np.zeros((np.ma.size(timesteps),2))
                retailer_trust_mean_std = np.zeros((np.ma.size(timesteps),2))
                if gossip_mode == "f":
                    gossip_trust_mean_std = np.zeros((np.ma.size(timesteps),2))

                supplier_price_mean_std = np.zeros((np.ma.size(timesteps),2))
                supplier_quality_mean_std = np.zeros((np.ma.size(timesteps),2))
                
                retailer_q_p_mean_std = np.zeros((np.ma.size(timesteps),2))
                supplier_q_p_mean_std = np.zeros((np.ma.size(timesteps),2))
                
                supplier_trust_mean_std = np.zeros((np.ma.size(timesteps),2))
                
                
                for i in range(0,np.ma.size(timesteps)):
                    retailer_price_mean_std[i,0] = np.mean(retailer_price[i,:])
                    retailer_price_mean_std[i,1] = np.std(retailer_price[i,:])
                    retailer_quality_mean_std[i,0] = np.mean(retailer_quality[i,:])
                    retailer_quality_mean_std[i,1] = np.std(retailer_quality[i,:])
                    retailer_trust_mean_std[i,0] = np.mean(retailer_trust[i,:])
                    retailer_trust_mean_std[i,1] = np.std(retailer_trust[i,:])
                    if gossip_mode == "f":
                        gossip_trust_mean_std[i,0] = np.mean(gossip_trust[i,:])
                        gossip_trust_mean_std[i,1] = np.std(gossip_trust[i,:])
                    
                    retailer_q_p_mean_std[i,0] = np.mean(retailer_quality_price[i,:])
                    retailer_q_p_mean_std[i,1] = np.std(retailer_quality_price[i,:])

                    supplier_price_mean_std[i,0] = np.mean(supplier_price[i,:])
                    supplier_price_mean_std[i,1] = np.std(supplier_price[i,:])
                    supplier_quality_mean_std[i,0] = np.mean(supplier_quality[i,:])
                    supplier_quality_mean_std[i,1] = np.std(supplier_quality[i,:])

                    supplier_trust_mean_std[i,0] = np.mean(supplier_trust[i,:])
                    supplier_trust_mean_std[i,1] = np.std(supplier_trust[i,:])
                    
                    supplier_q_p_mean_std[i,0] = np.mean(supplier_quality_price[i,:])
                    supplier_q_p_mean_std[i,1] = np.std(supplier_quality_price[i,:])
                
                # add mean and stdev data to list for this run
                retailer_run_mean_list = [directory, timesteps, retailer_price_mean_std, retailer_quality_mean_std, retailer_trust_mean_std, retailer_q_p_mean_std]
                if gossip_mode == "f":
                    retailer_run_mean_list.append(gossip_trust_mean_std)
                supplier_run_mean_list = [directory, timesteps, supplier_price_mean_std, supplier_quality_mean_std, supplier_q_p_mean_std]

                supplier_run_mean_list.append(supplier_trust_mean_std)
                
                retailer_data.append(retailer_run_list)
                retailer_mean_data.append(retailer_run_mean_list)
                supplier_data.append(supplier_run_list)
                supplier_mean_data.append(supplier_run_mean_list)
                    
    return  retailer_data, retailer_mean_data, supplier_data, supplier_mean_data
            

## make supplier histograms
def supplier_inv_histograms(supplier_data):
    """
    Makes histograms of the initial, midway and final supplier inventories
    """
    try:
        os.mkdir("SupplierData")
    except OSError:
        print("Data file already exists")
    
    for run in supplier_data:
        name = run[0]
        timesteps = run[1]
        inventory = run[2]
        
        
        # plot initial values
        plt.hist(inventory[0,:])
        plt.title(name + " inventory at t=" + str(int(timesteps[0])))
        plt.xlabel("Inventory")
        plt.ylabel("Number of suppliers")
        plt.savefig("SupplierData/" + name + "Inventory" + str(int(timesteps[0]))+".png")
        plt.clf()
        
        # plot midway values
        index = int((len(timesteps)+1)/2)
        plt.hist(inventory[index,:])
        plt.title(name+ " inventory at t=" + str(timesteps[index]))
        plt.xlabel("Inventory")
        plt.ylabel("Number of suppliers")
        plt.savefig("SupplierData/" + name + "Inventory" + str(timesteps[index])+".png")
        plt.clf()
        
        # plot end values
        index = len(timesteps) - 1
        plt.hist(inventory[index,:])
        plt.title(name+ " inventory at t=" + str(timesteps[index]))
        plt.xlabel("Inventory")
        plt.ylabel("Number of suppliers")
        plt.savefig("SupplierData/" + name + "Inventory" + str(timesteps[index])+".png")
        plt.clf()
        
def retailer_inv_histograms(retailer_data):
    """
    Makes histograms of the initial, midway and final retailer inventories
    """
    try:
        os.mkdir("RetailerData")
    except OSError:
        print("Data file already exists")
        
    for run in retailer_data:
        name = run[0]
        timesteps = run[1]
        inventory = run[2]
        
        
        # plot initial values
        plt.hist(inventory[0,:])
        plt.title(name + " inventory at t=" + str(int(timesteps[0])))
        plt.xlabel("Inventory")
        plt.ylabel("Number of suppliers")
        plt.savefig("RetailerData/" + name + "Inventory" + str(int(timesteps[0]))+".png")
        plt.clf()
        
        # plot midway values
        index = int((len(timesteps)+1)/2)
        plt.hist(inventory[index,:])
        plt.title(name+ " inventory at t=" + str(timesteps[index]))
        plt.xlabel("Inventory")
        plt.ylabel("Number of suppliers")
        plt.savefig("RetailerData/" + name + "Inventory" + str(timesteps[index])+".png")
        plt.clf()
        
        # plot end values
        index = len(timesteps) - 1
        plt.hist(inventory[index,:])
        plt.title(name+ " inventory at t=" + str(timesteps[index]))
        plt.xlabel("Inventory")
        plt.ylabel("Number of suppliers")
        plt.savefig("RetailerData/" + name + "Inventory" + str(timesteps[index])+".png")
        plt.clf()

def retailer_mean_plotter(retailer_mean_data):
    """
    Makes a Q/P plot over time for retailers
    """
    try:
        os.mkdir("RetailerData")
    except OSError:
        print("Data file already exists")
    
    timesteps = retailer_mean_data[0][1]
    
    # create arrays to have the mean quality/price and error over time for each run
    means_QP = np.zeros((len(retailer_mean_data),len(timesteps)))
    stdevs_QP = np.zeros((len(retailer_mean_data),len(timesteps)))
    
    # create arrays to have mean trust and error over time for each run
    means_trust = np.zeros((len(retailer_mean_data),len(timesteps)))
    stdevs_trust = np.zeros((len(retailer_mean_data),len(timesteps)))
    
    k = 0
    
    for run in retailer_mean_data:
        name = run[0]
        timesteps = run[1]
        QP = run[5]
        trust = run[4]
        
        # add mean values over time
        for i in range(0, len(timesteps)):
            means_QP[k,i] = QP[i,0]
            stdevs_QP[k,i] = QP[i,1]
            means_trust[k,i] = trust[i,0]
            stdevs_trust[k,i] = trust[i,1]
        k+=1
        
        # graph quality over price
        plt.errorbar(timesteps, QP[:,0], yerr=QP[:,1], fmt='k.', capsize=2)
        plt.title(name + " Quality/Price over time")
        plt.xlabel("Step number")
        plt.ylabel("Quality/Price")
        plt.savefig("RetailerData/" + name + "Quality_Price.png")
        plt.clf()
        
        # graph trust
        plt.errorbar(timesteps, trust[:,0], yerr = trust[:,1], fmt = 'k.', capsize=2)
        plt.title(name + " trust in retailers over time")
        plt.xlabel("Step number")
        plt.ylabel("Trust")
        plt.savefig("RetailerData/" + name + "Trust.png")
        plt.clf()
    
    mean_QP_allruns = np.zeros(np.ma.size(means_QP,1))
    error_QP_allruns =np.zeros(np.ma.size(means_QP,1)) 
    mean_trust_allruns= np.zeros(np.ma.size(means_QP,1))
    error_trust_allruns= np.zeros(np.ma.size(means_QP,1))
    
    # calculate mean and stdev QP over all runs
    for i in range(0, np.ma.size(means_QP,1)):
        mean_QP_allruns[i] = np.mean(means_QP[:,i])
        error_QP_allruns[i] = (1/len(retailer_mean_data))*math.sqrt(np.sum(np.square(stdevs_QP[:,i])))
        mean_trust_allruns[i] = np.mean(means_trust[:,i])
        error_trust_allruns[i] = (1/len(retailer_mean_data))*math.sqrt(np.sum(np.square(stdevs_QP[:,i])))
    
    # graph QP for all runs
    plt.errorbar(timesteps, mean_QP_allruns, yerr = error_QP_allruns, fmt= 'k.', capsize=2)
    plt.title("Mean Quality/Price over time")
    plt.xlabel("Step number")
    plt.ylabel("Quality/Price")
    plt.savefig("RetailerData/Overall_Quality_Price.png")
    plt.clf()

    
    # graph trust for all runs
    plt.errorbar(timesteps, mean_trust_allruns, yerr = error_trust_allruns, fmt= 'k.', capsize=2)
    plt.title("Mean trust over time")
    plt.xlabel("Step number")
    plt.ylabel("Trust")
    plt.savefig("RetailerData/Overall_Trust.png")
    plt.clf()

    

## read command line
gossip_mode = sys.argv[1] # f friendly, p public, 0 off

retailer_data, retailer_mean_data, supplier_data, supplier_mean_data = get_data(gossip_mode)

supplier_inv_histograms(supplier_data)
retailer_inv_histograms(retailer_data)
retailer_mean_plotter(retailer_mean_data)
