
def blob(counter):
    if counter > 5:
        return 1
    ret = blob (counter + 1) + counter
    return ret

if __name__ == '__main__':
    blob(0)
