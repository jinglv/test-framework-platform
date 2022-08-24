import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/users/login',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/api/users/info',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/api/users/logout',
    method: 'delete'
  })
}
