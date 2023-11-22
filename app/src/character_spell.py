from data import get_connection
import pymysql
import asyncio

from src import Character

class CharacterSpell(Character):
    def __init__(self, user_id=None, character_id=None):
        super().__init__(user_id=user_id, character_id=character_id)
        self._spells = []
    
    async def exists_specific_spell(self, spell_id):
        try:
            if self.character_id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_habilidade_personagem FROM habilidade_personagem WHERE id_habilidade = %s and id_personagem = %s)"
                        await mycursor.execute(query, (spell_id,self.character_id,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def exists_spell(self):
        try:
            if self.character_id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_habilidade_personagem FROM habilidade_personagem WHERE id_personagem = %s)"
                        await mycursor.execute(query, (self.character_id,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def insert_spell(self,spell_id):
        try:
            if self.character_id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO habilidade_personagem(id_personagem,id_habilidade) VALUES(%s,%s);"
                        await mycursor.execute(query, (self.character_id,spell_id))
                        await conn.commit()
                        return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def update_spell(self,spell_id,character_id_spell):
        try:
            if self.character_id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """UPDATE habilidade_personagem
                        SET id_habilidade=%s
                        WHERE id_habilidade_personagem=%s;"""
                        await mycursor.execute(query, (spell_id,character_id_spell))
                        await conn.commit()
                        return True
            return False
        except Exception as e:
            print(e)
            return False    
        
    async def delete_spell(self,character_id_spell):
        try:
            if self.character_id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from habilidade_personagem
                        WHERE id_habilidade=%s and id_personagem = %s;"""
                        await mycursor.execute(query, (character_id_spell, self.character_id))
                        await conn.commit()
                        return True
            return False
        except Exception as e:
            print(e)
            return False
        
    async def load_spells(self):
        try:
            if self.character_id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT hb.id_habilidade, hb.nome_habilidade, hb.nome_atributo, hb.nivel_habilidade, hb.tipo_dano, hb.qtd_dados, hb.lados_dados, hb.adicional_por_nivel, hb.link_detalhes, hp.id_habilidade_personagem
                        FROM habilidade_personagem hp
                        JOIN habilidade hb ON hp.id_habilidade = hb.id_habilidade
                        WHERE hp.id_personagem = %s;"""
                        await mycursor.execute(query, (self.character_id,))
                        result = await mycursor.fetchall()
                        if result:
                            for row in result:
                                habilidade = {
                                    'id_habilidade': row[0],
                                    'nome_habilidade': row[1],
                                    'nome_atributo': row[2],
                                    'nivel_habilidade': row[3],
                                    'tipo_dano': row[4],
                                    'qtd_dados': row[5],
                                    'lados_dados': row[6],
                                    'adicional_por_nivel': row[7],
                                    'link_detalhes': row[8],
                                    'id_habilidade_personagem': row[9]
                                }
                                self.spell = habilidade              
                            return True
            return False
        except Exception as e:
            print(e)
            return False
        
    @property
    def spell(self, value):
        return self._spells[value]
    
    @property
    def spells(self):
        return self._spells  
    
    @spell.setter
    def spell(self,value):
        self._spells.append(value)