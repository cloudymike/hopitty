
# From http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html

import sqlalchemy

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import recipeReader
import xml.dom.minidom

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=False)


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    stages = Column(String)
    equipment = Column(String)
    bsmx = Column(String)

    def __repr__(self):
        return "<User(name='%s')>" % (self.name)

    def getName(self):
        return(self.name)

    def getEquipment(self):
        return(self.equipment)

    def getBSMXdoc(self):
        return(xml.dom.minidom.parseString(self.bsmx))

    def getBSMXstring(self):
        return(self.bsmx)


class RecipeList():
    def __init__(self):
        Base.metadata.create_all(engine)

        #session_factory = sessionmaker(bind=engine)
        #Session = scoped_session(session_factory)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.fixednamelist = []

        print "=== RecipeList init DONE==="

    def readBMXdoc(self, doc):
        cloudRecipes = doc.getElementsByTagName("Cloud")
        for recipe in cloudRecipes:
            name = recipeReader.bsmxReadString(recipe, "F_R_NAME")
            print "....reading ", name
            print recipe
            xmlstring = recipe.toxml()
            if self.session.query(Recipe).filter_by(name=name).first() is None:
                equipment = recipeReader.bsmxReadString(recipe, "F_E_NAME")
                r = Recipe(name=name,
                           equipment=equipment,
                           bsmx=xmlstring)
                self.session.add(r)
                self.session.commit()
        print "==== Recipelist read ===="
        self.printNameList()
        self.fixednamelist = self.getNameList()
        print "========================="

    def printNameList(self):
        """ Writes a list of all the recipe names"""

        for instance in self.session.query(Recipe).order_by(Recipe.name):
            print instance.name

    def getlist(self):
        return(self.getNameList())

    def getNameList(self):
        """ Returns a list of all the recipe names"""
        namelist = []
        for instance in self.session.query(Recipe).order_by(Recipe.name):
            namelist.append(instance.name)
        return(namelist)

    def getFixedNameList(self):
        """
        DEBUGGING
        Returns a list of all the recipe names as in the fixednamelist
        For debugging when sql in multithread not working
        """
        return(self.fixednamelist)

    def getRecipe(self, name):
        return(self.getRecipeByName(name))

    def getRecipeByName(self, name):
        e = self.session.query(Recipe).filter_by(name=name).first()
        return(e)

    def deleteRecipe(self, name):
        self.deleteRecipeByName(name)

    def deleteRecipeByName(self, name):
        e = self.session.query(Recipe).filter_by(name=name).first()
        self.session.delete(e)

    def readBeerSmithFile(self, fileName):
        bsmxFD = open(fileName)
        bsmxRawData = bsmxFD.read()
        bsmxFD.close()
        bsmxCleanData = bsmxRawData.replace('&', 'AMP')

        doc = xml.dom.minidom.parseString(bsmxCleanData)
        return(doc)

    def readBeerSmith(self, fileName):
        doc = self.readBeerSmithFile(fileName)
        self.readBMXdoc(doc)
