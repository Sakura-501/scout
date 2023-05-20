from .getStaticFeature import *
from .getDynamicFeature import *

class getData:
    DyFeatureGetter = GetDynamicFeature()
    staticFeatureGetter = GetStaticFeature()

    def getNormalData(self,fullPath):
        num = 0
        fullPathList = []
        finalFile=[]
        vectorList = []
        for root, dirs, files in os.walk(fullPath):
            # print(root)
            # print(dirs)
            # print(files)
            for filename in files:
                if filename.endswith('.php'):
                    try:
                        fullPathList.append(f"{root}\\{filename}")
                    except:
                        continue
        for filepath in fullPathList:
            try:
                vec = []
                IC = self.staticFeatureGetter.getIC(filepath)
                f1, f2, f3, f4 = self.staticFeatureGetter.getKeywords(filepath)
                entropy = self.staticFeatureGetter.getEntropy(filepath)
                vec.append(IC)
                vec.append(f1)
                vec.append(f2)
                vec.append(f3)
                vec.append(f4)
                vec.append(entropy)
                opcodes = self.DyFeatureGetter.getOPCode(filepath)
                vec += self.DyFeatureGetter.textrank_all(opcodes)
                vec.append(0)
                num += 1
                vectorList.append(vec)
                finalFile.append(filepath)
            except:
                print(f'ERROR:{filepath}')
        return vectorList,finalFile,num

    def getWebshellData(self,fullPath):
        num = 0
        finalFile=[]
        fullPathList = []
        vectorList = []
        for root, dirs, files in os.walk(fullPath):
            # print(root)
            # print(dirs)
            # print(files)
            for filename in files:
                if filename.endswith('.php'):
                    try:
                        fullPathList.append(f"{root}\\{filename}")
                    except:
                        continue
        print(fullPathList)
        for filepath in fullPathList:
            try:
                vec = []
                IC = self.staticFeatureGetter.getIC(filepath)
                f1, f2, f3, f4 = self.staticFeatureGetter.getKeywords(filepath)
                entropy = self.staticFeatureGetter.getEntropy(filepath)
                vec.append(IC)
                vec.append(f1)
                vec.append(f2)
                vec.append(f3)
                vec.append(f4)
                vec.append(entropy)
                opcodes = self.DyFeatureGetter.getOPCode(filepath)
                vec += self.DyFeatureGetter.textrank_all(opcodes)
                vec.append(1)
                num += 1
                vectorList.append(vec)
                finalFile.append(filepath)
            except:
                print(f'ERROR:{filepath}')
        return vectorList,finalFile,num  # 特征值（99：6+92+1） 路径名 php文件数量

# if __name__ == '__main__':
#     DataGetter=getData()
#     vec_list,white=DataGetter.getNormalData('D:\\newDesktop\\wind\\scout\\traindata\\white-traindata')
#     print(vec_list)
#     print(white)
