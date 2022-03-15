# pyscript-mi-smartlock
用于小米智能门锁的自动化脚本，基于pyscript。

# 已适配的型号
smartlock_mi_t1pro.py: 小米全自动智能门锁 Pro (loock.lock.t1pro)

# 使用方法
    ```configuration.yaml
    pyscript:
      allow_all_imports: false
      hass_is_global: false
    sensor: !include_dir_merge_list sensor/
	# Debug
	logger:
      default: error
      logs:
        custom_components.pyscript.file.[file_name]: debug
    ```