#!/usr/bin/env python3
# Generated by https://diagrams.mingrammer.com
#  > pip install diagrams
#  > python diagram.py
from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Functions
from diagrams.gcp.database import SQL, Memorystore
from diagrams.k8s.compute import Pod
from diagrams.onprem.compute import Server as AuthProvider
from diagrams.programming.language import Go
import os

# find docs/ directory to save png to
docs_dir = os.path.dirname(os.path.realpath(__file__))
output = os.path.join(docs_dir, "architecture")

with Diagram("Trident", filename=output, direction="LR", show=False):

    go = Go("operator")

    with Cluster("GCP Project"):

        with Cluster("Orchestrator"):
            with Cluster("argo"):
                api = Pod("api")

            with Cluster("Event Driven"):
                producer = Pod("producer")
                consumer = Pod("consumer")
        
            db = SQL("db")
            cache = Memorystore("redis")

        pubsub = PubSub("pubsub")

        go >> api
        api >> db
        api >> cache
        cache >> producer >> Edge(label="credentials", style="dashed") >> pubsub
        pubsub >> Edge(label="results", style="dashed") >> consumer >> db >> api

    with Cluster("Executors"):

        with Cluster("GCP Functions"):
            dispatch_gcp = Functions("dispatcher1")

        with Cluster("AWS Lambdas"):
            dispatch_aws = Functions("dispatcher2")
    
    with Cluster("Authentication Providers"):
        okta = AuthProvider("okta")
        o365 = AuthProvider("o365")

    pubsub >> Edge(label="credentials", style="dashed") >> dispatch_gcp
    dispatch_gcp >> Edge(label="results", style="dashed") >> pubsub

    dispatch_gcp >> okta
    dispatch_aws >> o365