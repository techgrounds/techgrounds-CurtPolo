#!/usr/bin/env python3

import aws_cdk as cdk

from final_project.final_project_stack import FinalProjectStack


app = cdk.App()
FinalProjectStack(app, "final-project")

app.synth()
