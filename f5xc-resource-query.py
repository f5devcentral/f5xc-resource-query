#!/usr/bin/env python3
# This script written to query F5XC via tenant API to enumerate resource usage 
# as well as provide single view (csv) on all required resources within tenant. 
# Currently only support resources for http_lb, routes, origin_pool, advertise_policy which
# commonly being used.
# Default provide views on usage metric
# 
# Author: Foo-Bang
# Date: 21 Dec 2022
# Note:
# - Default without argument will only collect usage for http_lb, routes, origin_pool and advertise_policy
#   Example: ./f5xc-resource-query.py
# - For details on specific resources (use -h for helps)
#   Example: 
#   ./f5xc-resource-query.py -r http_lb
#   ./f5xc-resource-query.py -r routes
#   ./f5xc-resource-query.py -r origin_pool
#   ./f5xc-resource-query.py -r advertise_policy
# - Update the tenant ID and the respective API Key.
# 
import argparse
import requests
import json
import base64
import warnings
import sys
warnings.filterwarnings("ignore")


# Global Variable
tenant_url = 'https://--your-tenant-id---.console.ves.volterra.io'
api_token = 'xxxxxxxxxxx' # API token for xxxxxxx

usage_only = 'true' # Default to print usage only
api_ns = tenant_url + '/api/web/namespaces'
headers = {
    'Content-Type': 'application/json',
     'Authorization': 'APIToken ' + api_token
}

################################################
# Function to list HTTP LB by namespace
################################################
def get_http_lb (ns,usage):

        api_http_lb = tenant_url + '/api/config/namespaces/' + ns + '/http_loadbalancers'
        req_http_lb = requests.get(api_http_lb, headers=headers, verify=False)
        data_http_lb = req_http_lb.json()
        items_http_lb = data_http_lb['items']

        if usage.casefold() == 'true':
            resource_util =  str(len(items_http_lb))
            #print (ns + ',' + str(len(items_http_lb)))
            #return str(len(items_http_lb)
        else:
            resource_util = 0
            if (len(items_http_lb) == 0):
                print (ns + ',nill,nill')
            else:
                for item_http_lb in items_http_lb:
                        http_lb = item_http_lb['name']
                        api_http_lb_domain = tenant_url + '/api/config/namespaces/' + ns + '/http_loadbalancers/' + http_lb
                        req_http_lb_domain = requests.get(api_http_lb_domain, headers=headers, verify=False)
                        data_http_lb_domain = req_http_lb_domain.json()
                        #items_http_lb_domain = str(data_http_lb_domain['spec']['domains'][1])
                        items_http_lb_domains = data_http_lb_domain['spec']['domains']
        
                        for items_http_lb_domain in items_http_lb_domains:
                            print (ns + ',' + http_lb + ',' + items_http_lb_domain)
        
                        #print(ns + ',' + http_lb)
        return resource_util
################################################

    
################################################
# Function to list routes by namespace
################################################
def get_routes (ns,usage):
        api_routes = tenant_url + '/api/config/namespaces/' + ns + '/routes'
        req_routes = requests.get(api_routes, headers=headers, verify=False)
        data_routes = req_routes.json()
        items_routes = data_routes['items']

        if usage.casefold() == 'true':
            resource_util =  str(len(items_routes))
        else:
            resource_util = 0
            if (len(items_routes) == 0):
                print (ns + ',nill,nill')
            else:
                for item_route in items_routes:
                        route = item_route['name']
                        print(ns + ',' + route)
        return resource_util
################################################

################################################
# Function to list Origin Pool by namespace
################################################
def get_origin_pool (ns,usage):
        api_origin_pool = tenant_url + '/api/config/namespaces/' + ns + '/origin_pools'
        req_origin_pool = requests.get(api_origin_pool, headers=headers, verify=False)
        data_origin_pool = req_origin_pool.json()
        items_origin_pool = data_origin_pool['items']

        if usage.casefold() == 'true':
            resource_util =  str(len(items_origin_pool))
        else:
            resource_util = 0
            if (len(items_origin_pool) == 0):
                print (ns + ',nill,nill')
            else:
                for item_origin_pool in items_origin_pool:
                        origin_pool = item_origin_pool['name']
                        print(ns + ',' + origin_pool)
        return resource_util
################################################


################################################
# Function to list advertise policy by namespace
################################################
def get_advertise_policys (ns,usage):
        api_advertise_policys = tenant_url + '/api/config/namespaces/' + ns + '/advertise_policys'
        req_advertise_policys = requests.get(api_advertise_policys, headers=headers, verify=False)
        data_advertise_policys = req_advertise_policys.json()
        items_advertise_policys = data_advertise_policys['items']

        if usage.casefold() == 'true':
            resource_util =  str(len(items_advertise_policys))
        else:
            resource_util = 0
            if (len(items_advertise_policys) == 0):
                print (ns + ',nill,nill')
            else:
                for item_advertise_policy in items_advertise_policys:
                        advertise_policy = item_advertise_policy['name']
                        print(ns + ',' + advertise_policy)
        return resource_util
################################################

################################################
# Function to list clusters by namespace
################################################
def get_clusters (ns,usage):
        api_clusters = tenant_url + '/api/config/namespaces/' + ns + '/clusters'
        req_clusters = requests.get(api_clusters, headers=headers, verify=False)
        data_clusters = req_clusters.json()
        items_clusters = data_clusters['items']

        if usage.casefold() == 'true':
            resource_util =  str(len(items_clusters))
        else:
            resource_util = 0
            if (len(items_clusters) == 0):
                print (ns + ',nill,nill')
            else:
                for item_cluster in items_clusters:
                        cluster = item_cluster['name']
                        print(ns + ',' + cluster)
        return resource_util
################################################


##############
### Main
##############
parser = argparse.ArgumentParser(description='F5XC Tenant Resource Usage')
parser.add_argument('-r','--resources', help='Type of resource - http_lb / routes / origin_pool / advertise_policy / clusters', required=False)

args = vars(parser.parse_args())
resources = args ['resources']

req_ns = requests.get(api_ns, headers=headers, verify=False)
data_ns = req_ns.json()
items_ns = data_ns['items']

if args['resources'] == 'http_lb':
    print ('NAMESPACE,HTTP_LB,DOMAIN')
    for item_ns in items_ns:
        ns = item_ns['name']
        http_lb_usage = get_http_lb(ns,'false')
elif args['resources'] == 'routes':
    print ('NAMESPACE,ROUTES')
    for item_ns in items_ns:
        ns = item_ns['name']
        route_usage = get_routes(ns,'false')
elif args['resources'] == 'origin_pool':
    print ('NAMESPACE,ORIGIN-POOL')
    for item_ns in items_ns:
        ns = item_ns['name']
        origin_pool_usage = get_origin_pool(ns,'false')
elif args['resources'] == 'advertise_policy':
    print ('NAMESPACE,ADVERTISE-POLICY')
    for item_ns in items_ns:
        ns = item_ns['name']
        advertise_policy_usage = get_advertise_policys(ns,'false')
elif args['resources'] == 'clusters':
    print ('NAMESPACE,CLUSTERS')
    for item_ns in items_ns:
        ns = item_ns['name']
        advertise_policy_usage = get_clusters(ns,'false')        
else:
    usage_only = 'true'
    print ('############################################################################')
    print ('##                         Quota Usage per namespaces                     ##')
    print ('############################################################################')
    print ('{:20s} {:8s} {:8s} {:8s} {:8s} {:8s}'.format('Namespace','HTTP_LB','Routes','origin_pool','advertise_policy','clusters'))    
    for item_ns in items_ns:
        ns = item_ns['name']
        http_lb_usage = get_http_lb(ns,usage_only)
        route_usage = get_routes(ns,usage_only)
        origin_pool_usage = get_origin_pool(ns,usage_only)
        advertise_policy_usage = get_advertise_policys(ns,usage_only)
        cluster_usage = get_clusters(ns,usage_only)

        print ('{:20s} {:10s} {:10s} {:10s} {:15s} {:10s}'.format(ns,http_lb_usage,route_usage,origin_pool_usage,advertise_policy_usage,cluster_usage))
