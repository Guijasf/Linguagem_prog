import pandas as pd

from sqlalchemy import (
    create_engine,
    text,
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Float,
    insert,
    update,
    select,
    func,
    ForeignKey,
)

from sqlalchemy.orm import (
    declarative_base,
    mapped_column,
    Mapped,
    relationship,
    sessionmaker,
)


# ==========================================================
# NÍVEL 1 - SQL PURO COM SEGURANÇA
# ==========================================================

print("\n" + "=" * 60)
print("NÍVEL 1 - SQL PURO COM SEGURANÇA")
print("=" * 60)


# ----------------------------------------------------------
# Passo 1 - Criando conexão com SQLite
# ----------------------------------------------------------

engine = create_engine("sqlite:///sistema_rh.db")

print("\nBanco de dados conectado com sucesso!")


# ----------------------------------------------------------
# Passo 2 - Criando tabela funcionarios usando SQL puro
# ----------------------------------------------------------

with engine.begin() as conn:

    conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL,
                cargo VARCHAR(100) NOT NULL,
                salario REAL NOT NULL
            )
            """
        )
    )

print("Tabela 'funcionarios' criada/verificada com sucesso.")


# ----------------------------------------------------------
# Passo 3 - Inserção segura usando parâmetros
# ----------------------------------------------------------

# Simulação dos dados recebidos de um formulário web
nome_formulario = "João Silva"
cargo_formulario = "Desenvolvedor Júnior"
salario_formulario = 3500.00


with engine.begin() as conn:

    conn.execute(
        text(
            """
            INSERT INTO funcionarios (nome, cargo, salario)
            VALUES (:nome, :cargo, :salario)
            """
        ),
        {
            "nome": nome_formulario,
            "cargo": cargo_formulario,
            "salario": salario_formulario,
        },
    )


print("Funcionário inserido com segurança!")


# ----------------------------------------------------------
# Passo 4 - Consultando dados com Pandas
# ----------------------------------------------------------

with engine.connect() as conn:

    dataframe_funcionarios = pd.read_sql_query(
        text("SELECT * FROM funcionarios"),
        conn,
    )


print("\nFuncionários cadastrados:")
print(dataframe_funcionarios)


# ==========================================================
# NÍVEL 2 - SQLALCHEMY CORE
# ==========================================================

print("\n" + "=" * 60)
print("NÍVEL 2 - SQLALCHEMY CORE")
print("=" * 60)


# ----------------------------------------------------------
# Passo 1 - Criando tabela projetos com SQLAlchemy Core
# ----------------------------------------------------------

metadata = MetaData()


projetos = Table(
    "projetos",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),

    Column(
        "nome",
        String(100),
        nullable=False,
    ),

    Column(
        "responsavel",
        String(100),
        nullable=False,
    ),

    Column(
        "orcamento",
        Float,
        nullable=False,
    ),
)


metadata.create_all(engine)

print("\nTabela 'projetos' criada/verificada com sucesso.")


# ----------------------------------------------------------
# Passo 2 - Bulk Insert
# ----------------------------------------------------------

lista_de_projetos = [

    {
        "nome": "Sistema de RH",
        "responsavel": "João Silva",
        "orcamento": 15000.00,
    },

    {
        "nome": "Portal Corporativo",
        "responsavel": "Maria Souza",
        "orcamento": 22000.00,
    },

    {
        "nome": "Aplicativo Mobile",
        "responsavel": "Carlos Santos",
        "orcamento": 30000.00,
    },

]


with engine.begin() as conn:

    conn.execute(
        insert(projetos),
        lista_de_projetos,
    )


print("Projetos inseridos em lote com sucesso!")


# ----------------------------------------------------------
# Recuperando a tabela funcionarios criada no Nível 1
# ----------------------------------------------------------

metadata_funcionarios = MetaData()


funcionarios = Table(
    "funcionarios",
    metadata_funcionarios,
    autoload_with=engine,
)


# ----------------------------------------------------------
# Inserindo funcionários extras para testar relatório
# ----------------------------------------------------------

funcionarios_extras = [

    {
        "nome": "Maria Oliveira",
        "cargo": "Desenvolvedor Júnior",
        "salario": 3800.00,
    },

    {
        "nome": "Carlos Souza",
        "cargo": "Desenvolvedor Pleno",
        "salario": 5500.00,
    },

    {
        "nome": "Ana Lima",
        "cargo": "Analista de RH",
        "salario": 4200.00,
    },

]


with engine.begin() as conn:

    conn.execute(
        insert(funcionarios),
        funcionarios_extras,
    )


# ----------------------------------------------------------
# Passo 3 - Aumento de salário
# Desenvolvedor Júnior recebe aumento de 10%
# ----------------------------------------------------------

with engine.begin() as conn:

    comando_reajuste = (

        update(funcionarios)

        .where(
            funcionarios.c.cargo
            == "Desenvolvedor Júnior"
        )

        .values(
            salario=funcionarios.c.salario * 1.10
        )

    )

    conn.execute(comando_reajuste)


print("\nReajuste de 10% aplicado aos Desenvolvedores Júnior.")


# ----------------------------------------------------------
# Mostrando funcionários depois do reajuste
# ----------------------------------------------------------

with engine.connect() as conn:

    resultado = conn.execute(
        select(funcionarios)
    )

    print("\nFuncionários após reajuste:")

    for funcionario in resultado:

        print(
            funcionario.id,
            funcionario.nome,
            funcionario.cargo,
            funcionario.salario,
        )


# ----------------------------------------------------------
# Passo 4 - Relatório salarial
# Média salarial agrupada por cargo
# ----------------------------------------------------------

consulta_media = (

    select(

        funcionarios.c.cargo,

        func.avg(
            funcionarios.c.salario
        ).label("media_salarial"),

    )

    .group_by(
        funcionarios.c.cargo
    )

)


with engine.connect() as conn:

    resultado_media = conn.execute(
        consulta_media
    )


    print("\nRELATÓRIO DE MÉDIA SALARIAL")
    print("-" * 45)


    for linha in resultado_media:

        print(
            f"Cargo: {linha.cargo}"
            f" | Média salarial: "
            f"R$ {linha.media_salarial:.2f}"
        )


# ==========================================================
# NÍVEL 3 - ORM
# ==========================================================

print("\n" + "=" * 60)
print("NÍVEL 3 - ORM")
print("=" * 60)


# ----------------------------------------------------------
# Passo 1 - Criando Base ORM
# ----------------------------------------------------------

Base = declarative_base()


# ----------------------------------------------------------
# Classe Departamento
# ----------------------------------------------------------

class Departamento(Base):

    __tablename__ = "departamentos"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    # Relacionamento com funcionários
    funcionarios: Mapped[list["FuncionarioORM"]] = relationship(
        "FuncionarioORM",
        back_populates="departamento",
    )


# ----------------------------------------------------------
# Classe FuncionarioORM
# ----------------------------------------------------------

class FuncionarioORM(Base):

    __tablename__ = "funcionarios_orm"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    cargo: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    salario: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )


    # Chave estrangeira
    departamento_id: Mapped[int] = mapped_column(
        ForeignKey("departamentos.id"),
        nullable=False,
    )


    # Relacionamento com Departamento
    departamento: Mapped["Departamento"] = relationship(
        "Departamento",
        back_populates="funcionarios",
    )


# ----------------------------------------------------------
# Criando tabelas ORM
# ----------------------------------------------------------

Base.metadata.create_all(engine)

print("\nTabelas ORM criadas/verificadas com sucesso!")


# ----------------------------------------------------------
# Passo 3 - Criando Session
# ----------------------------------------------------------

Session = sessionmaker(bind=engine)

sessao = Session()


try:

    # Criando departamento
    departamento_ti = Departamento(
        nome="TI"
    )


    # Criando funcionários
    funcionario1 = FuncionarioORM(
        nome="Lucas Ferreira",
        cargo="Desenvolvedor Backend",
        salario=6000.00,
    )


    funcionario2 = FuncionarioORM(
        nome="Fernanda Alves",
        cargo="Desenvolvedora Frontend",
        salario=5800.00,
    )


    funcionario3 = FuncionarioORM(
        nome="Rafael Gomes",
        cargo="Analista de Sistemas",
        salario=5200.00,
    )


    # Adicionando funcionários ao departamento
    departamento_ti.funcionarios.extend(
        [
            funcionario1,
            funcionario2,
            funcionario3,
        ]
    )


    # Adicionando departamento à sessão
    # Os funcionários são persistidos pelo relacionamento
    sessao.add(departamento_ti)


    # Salvando no banco
    sessao.commit()


    print(
        "\nDepartamento e funcionários "
        "salvos com sucesso!"
    )


    # ======================================================
    # Passo 4 - Consulta orientada a objetos
    # ======================================================

    consulta_ti = (

        select(FuncionarioORM)

        .join(FuncionarioORM.departamento)

        .where(
            Departamento.nome == "TI"
        )

    )


    funcionarios_ti = (

        sessao.execute(consulta_ti)

        .scalars()

        .all()

    )


    print("\nFUNCIONÁRIOS DO DEPARTAMENTO DE TI")
    print("-" * 50)


    for funcionario in funcionarios_ti:

        print(
            f"ID: {funcionario.id}"
        )

        print(
            f"Nome: {funcionario.nome}"
        )

        print(
            f"Cargo: {funcionario.cargo}"
        )

        print(
            f"Salário: R$ {funcionario.salario:.2f}"
        )

        print(
            f"Departamento: "
            f"{funcionario.departamento.nome}"
        )

        print("-" * 50)


finally:

    # Fechando sessão
    sessao.close()

    print("\nSessão encerrada.")


print("\n" + "=" * 60)
print("ATIVIDADE FINALIZADA")
print("=" * 60)