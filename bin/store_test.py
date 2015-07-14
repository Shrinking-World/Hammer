from time import sleep

from store import save, recall, expire, expiration, save_key, recall_key
from tst import run_diff_checks


def store_redis_test():
    lines = [
        recall('test_redis/name'),
        save  ('test_redis/name','Mark'),
        recall('test_redis/name'),
        save  ('test_redis/name','Eric'),
        recall('test_redis/name')
    ]
    return '\n'.join(lines)


def store_expiration_test():
    save  ('test_redis/expiration','Yeah'),
    save  ('test_redis/expiration1','Yeah'),
    expire('test_redis/expiration1',1),
    expire('test_redis/expiration',10),
    lines = [
        str(expiration('test_redis/expiration')),
        str(expiration('test_redis/expiration1')),
        str(recall('test_redis/expiration1')),
        str(sleep(1)),
        str(expiration('test_redis/expiration')),
        str(recall('test_redis/expiration1')),
    ]
    return '\n'.join(lines)


def store_missing_test():
    lines = [
        str(recall('test_redis/missing')),
        str(recall('test_redis/name'))
    ]
    return '\n'.join(lines)


def store_key_test():
    save_key('store_key_test', 42)
    return recall_key('store_key_test')


def store_checker():
    '''Execute all the desired diff tests'''
    my_tests = {
        'store-expiration': store_expiration_test,
        'store-key': store_key_test,
        'store-missing': store_missing_test,
        'store-redis': store_redis_test,
    }
    run_diff_checks('store', my_tests)


# Create a script that can be run from the tst
if __name__=='__main__':
    store_checker()