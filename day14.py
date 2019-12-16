# -*- coding: utf-8 -*-


class Recipe:

    def __init__(self, name, count=1, components=None):
        self.name = name
        self.count = count # material count in the recipe
        self.components = components

    def getOre(self):
        '''
        Return the number of ORE needed to build 1 of this material.
        '''
        print(self.name)
        if self.name == 'ORE':
            return self.count
        else:
            s = 0
            for comp, count in self.components:
                print('>%s %s' % (comp.name, count))
                s += (count * comp.getOre())
            return s


'''
Partant de la recette FUEL:

    Pour chaque recette:
        Pour chaque couple Ingredient/Quantité:
            Trouver la recette produisant le minimum nécessaire
                Recommencer
            Si seul ingrédient = ORE, retourner ORE
'''


ore = Recipe('ORE')
a = Recipe('A', 10, [(ore, 10)])
b = Recipe('B', 1, [(ore, 1)])
fuel = Recipe('FUEL', 1, [(a, 7), (b, 1)])

print(fuel.getOre())



# class Recipe(object):

#     ingredients = {} # {material: count}
#     result = [] # [material, count]

#     def addIngredient(self, mat, count):
#         self.ingredients[mat] = count
    
#     def setResult(self, mat, count):
#         self.result = [mat, count]
    
#     def __repr__(self):
#         return ', '.join(['%s %s' % (j, i) for i, j in self.ingredients.items()]) + ' => %s %s' % (self.result[1], self.result[0])


# if __name__ == '__main__':

#     with open(__file__.replace('.py', '.input'), 'r') as f:
#         recipes = [i.strip() for i in f.readlines()]

#     fuelRecipe = [i for i in recipes if i.endswith('FUEL')][0]

#     print(fuelRecipe)




