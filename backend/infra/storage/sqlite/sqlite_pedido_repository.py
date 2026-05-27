from backend.domain.repository.pedido_repository import PedidoRepository
from backend.infra.db import get_db

class SqlitePedidoRepository(PedidoRepository):
    def get_open_pedido(self, usuario_id):
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM Pedidos WHERE UsuarioId = ? AND Status = 'ABERTO' ORDER BY Id DESC LIMIT 1",
                (usuario_id,),
            ).fetchone()

    def create_open_pedido(self, usuario_id):
        with get_db() as conn:
            cur = conn.execute(
                "INSERT INTO Pedidos (UsuarioId, Status) VALUES (?, 'ABERTO')",
                (usuario_id,),
            )
            conn.commit()
            return cur.lastrowid

    def add_item_to_pedido(self, pedido_id, item_nome, item_foto, item_valor, quantidade, observacao):
        with get_db() as conn:
            conn.execute(
                """
                    INSERT INTO PedidoItens (PedidoId, ItemNome, ItemFoto, ItemValor, Quantidade, Observacao)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (pedido_id, item_nome, item_foto, float(item_valor), int(quantidade), observacao),
            )
            conn.commit()

    def get_open_pedido_items(self, usuario_id):
        with get_db() as conn:
            return conn.execute(
                """
                SELECT pi.Id as id,
                       pi.ItemNome as nome,
                       pi.ItemFoto as foto,
                       pi.ItemValor as valor,
                       pi.Quantidade as quantidade,
                       pi.Observacao as observacao
                FROM PedidoItens pi
                JOIN Pedidos p ON p.Id = pi.PedidoId
                WHERE p.UsuarioId = ? AND p.Status = 'ABERTO'
                ORDER BY pi.Id DESC
                """,
                (usuario_id,),
            ).fetchall()

    def delete_item_from_open_pedido(self, pedido_item_id, usuario_id):
        with get_db() as conn:
            conn.execute(
                """
                DELETE FROM PedidoItens
                WHERE Id = ?
                  AND PedidoId IN (
                    SELECT Id FROM Pedidos
                    WHERE UsuarioId = ? AND Status = 'ABERTO'
                  )
                """,
                (pedido_item_id, usuario_id),
            )
            conn.commit()

    def finalize_open_pedido(self, usuario_id):
        with get_db() as conn:
            conn.execute(
                """
                UPDATE Pedidos
                SET Status = 'FINALIZADO'
                WHERE UsuarioId = ? AND Status = 'ABERTO'
                """,
                (usuario_id,),
            )
            conn.commit()
