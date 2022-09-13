import request from '@/utils/request'

export function getProjectFiles(project_id) {
  return request({
    url: '/api/cases/' + project_id + '/files',
    method: 'get'
  })
}

export function syncProjectCase(project_id) {
  return request({
    url: '/api/cases/sync?project_id=' + project_id,
    method: 'get'
  })
}

export function getProjectCases(project_id, params) {
  return request({
    url: '/api/cases/' + project_id + '/cases',
    method: 'get',
    params
  })
}

export function getProjectSubdirectory(project_id, params) {
  return request({
    url: '/api/cases/' + project_id + '/subdirectory',
    method: 'get',
    params
  })
}

export function caseResult(case_id) {
  return request({
    url: '/api/cases/' + case_id + '/result',
    method: 'get'
  })
}

export function runningCase(case_id, data) {
  return request({
    url: '/api/cases/' + case_id + '/running',
    method: 'post',
    data
  })
}

