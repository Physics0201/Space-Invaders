elif vel == -20:
                for obj in objs: 
                    if laser.collision(obj):
                        objs.remove(obj)
                        print("work")
                        if laser in self.lasers:
                            self.lasers.remove(laser)
            elif laser.collision(objs) and vel == -10:
                objs.health -= 10
                if laser in self.lasers:
                    self.lasers.remove(laser)