import request from '@/utils/request'

export function getEnvs(project_id) {
  return request({
    url: '/api/env/' + project_id + '/list',
    method: 'get'
  })
}

export function createEnv(data) {
  return request({
    url: '/api/env/create',
    method: 'post',
    data
  })
}

export function updateEnv(env_id, data) {
  return request({
    url: '/api/env/' + env_id,
    method: 'put',
    data
  })
}

export function envDetail(env_id) {
  return request({
    url: '/api/env/' + env_id,
    method: 'get'
  })
}

export function deleteEnv(evn_id) {
  return request({
    url: '/api/env/' + evn_id,
    method: 'delete'
  })
}

export function getAllEnvs(params) {
  return request({
    url: '/api/env/list',
    method: 'get',
    params
  })
}
