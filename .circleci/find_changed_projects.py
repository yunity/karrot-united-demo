#!/usr/bin/env python3
# -*- coding: utf-8 -*-

projects = ['client', 'server', 'docs']

import requests
import subprocess
import os

def get_workflows(branch):
    r = requests.get('https://circleci.com/api/v1.1/project/github/yunity/karrot-frontend/tree/{}?limit=100'.format(branch))
    j = r.json()
    
    workflows = {}
    workflows_sorted = []
    for job in j:
        w_id = job['workflows']['workflow_id']
        if not workflows.get(w_id):
            workflows[w_id] = {'jobs': []}
        workflows[w_id]['jobs'].append(job)
        if w_id not in workflows_sorted:
            workflows_sorted.append(w_id)
            
    return [workflows[w_id] for w_id in workflows_sorted]


def get_first_finished_workflow(workflows):
    workflow = None
    for workflow in workflows:
        workflow['finished'] = all(e['lifecycle']=='finished' for e in workflow['jobs'])
        workflow['commit'] = workflow['jobs'][0]['vcs_revision']
        for project in projects:
            project_jobs = [j for j in workflow['jobs'] if j['workflows']['job_name'].startswith(project)]
            workflow[project] = {
                'success': all(e['outcome']=='success' for e in project_jobs)
            }
        if workflow['finished']:
            break

    return workflow
        
            
branch = os.environ.get('CIRCLE_BRANCH')
workflow = None
if branch:
    workflow = get_first_finished_workflow(get_workflows(branch))
if workflow is None:
    workflow = get_first_finished_workflow(get_workflows('master'))    

changed_files = subprocess.check_output(['git', 'diff', workflow['commit'], 'HEAD', '--name-only']).decode().split()
    
output = []
changed_tpl = 'export {project}_CHANGED={val}'
success_tpl = 'export {project}_SUCCESS={val}'
for project in projects:
    changed = any(f.startswith(project + '/') for f in changed_files)
    success = workflow[project]['success']
    output.append(changed_tpl.format(project=project.upper(), val=1 if changed else 0))
    output.append(success_tpl.format(project=project.upper(), val=1 if success else 0))
    
print('\n'.join(output))
    