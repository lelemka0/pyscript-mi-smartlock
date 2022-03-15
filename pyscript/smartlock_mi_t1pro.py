from homeassistant.const import EVENT_STATE_CHANGED

action_entity_id = 'sensor.xxxxxxxxxxxx_action' #修改为你的门锁action entity_id
smartlock_door_entity_id = 'sensor.smartlock_door'
smartlock_state_entity_id = 'sensor.smartlock_state'
smartlock_method_entity_id = 'sensor.smartlock_method'
smartlock_user_entity_id = 'sensor.smartlock_user'

@event_trigger(EVENT_STATE_CHANGED, f"entity_id == '{action_entity_id}'") 
def state_changed(entity_id=None, new_state=None, old_state=None):
    #log.debug(f"got arguments {kwargs}")
    #log.info(f"entity {entity_id} changed from {old_state} to {new_state}")
    if new_state.state == 'lock':
        state.set(
            var_name = smartlock_state_entity_id,
            value = get_lock_action(new_state.attributes['action_id']),
            meaasge = new_state.attributes['message'],
            update_time = new_state.last_updated
        )
        state.set(
            var_name = smartlock_method_entity_id,
            value = get_lock_method(new_state.attributes['method_id']),
            update_time = new_state.last_updated
        )
        state.set(
            var_name = smartlock_user_entity_id,
            value = get_lock_key(new_state.attributes['key_id']),
            update_time = new_state.last_updated
        )
        #Additional
        if new_state.attributes['action_id'] == 0 or \
           new_state.attributes['action_id'] == 4:
            state.set(
                var_name = smartlock_door_entity_id,
                value = '开启',
                icon = 'mdi:door-open',
                meaasge = 'Door is open (Updated by Lock Unlock)',
                update_time = new_state.last_updated
            )
    
    if new_state.state == 'door':
        state.set(
            var_name = smartlock_door_entity_id,
            value = get_door_action(new_state.attributes['action_id']),
            meaasge = new_state.attributes['message'],
            update_time = new_state.last_updated
        )
        #Additional
        if new_state.attributes['action_id'] == 1:
            state.set(
                var_name = smartlock_door_entity_id,
                icon = 'mdi:door-closed-lock'
            )
            state.set(
                var_name = smartlock_state_entity_id,
                value = '上锁',
                meaasge = 'Lock (Updated by Door Close)',
                update_time = new_state.last_updated
            )
            state.set(
                var_name = smartlock_method_entity_id,
                value = '关门自动上锁',
                update_time = new_state.last_updated
            )
            state.set(
                var_name = smartlock_user_entity_id,
                value = '自动操作',
                update_time = new_state.last_updated
            )
        else:
            state.set(
                var_name = smartlock_door_entity_id,
                icon = 'mdi:door-open'
            )

def get_lock_key(key_id):
    numbers = {
        'ffffffff' : "未知操作者",
        'DEADBEEF' : "无效操作者",
        0 : "管理员",
        1 : "爸爸的指纹"
    }
    return numbers.get(key_id, f'Unknown key_id: {key_id}')

def get_door_action(action_id):
    numbers = {
        0 : "开启", #Door is open
        1 : "关闭", #Door is closed
        2 : "超时未关闭", #Timeout is not closed
        3 : "有人敲门", #Knock on the door
        4 : "正被破坏", #Breaking the door
        5 : "门被卡住" #Door is stuck
    }
    return numbers.get(action_id, f'Unknown action_id: {action_id}')

def get_lock_action(action_id):
    numbers = {
        0 : "门外开锁", #Unlock outside the door
        1 : "上锁", #Lock
        2 : "反锁", #Turn on anti-lock
        3 : "解除反锁", #Turn off anti-lock
        4 : "门内开锁", #Unlock inside the door
        5 : "门内上锁", #Lock inside the door
        6 : "开启童锁", #Turn on child lock
        7 : "关闭童锁" #Turn off child lock
    }
    return numbers.get(action_id, f'Unknown action_id: {action_id}')

def get_lock_method(method_id):
    numbers = {
        0 : "蓝牙", #bluetooth
        1 : "密码", #password
        2 : "指纹", #biological
        3 : "钥匙", #key
        4 : "转盘", #turntable
        5 : "NFC", #nfc
        6 : "一次性密码", #one-time password
        7 : "双重验证", #two-step verification
        8 : "强制", #coercion
        10 : "手动", #manual
        11 : "自动" #automatic
    }
    return numbers.get(method_id, f'Unknown method_id: {method_id}')
