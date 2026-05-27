from typing import List
from backend.domain.repository.pedido_repository import PedidoRepository
from backend.domain.entity.pedido import Pedido
from backend.domain.entity.pedido_item import PedidoItem
from backend.infra.storage.sqlite.model.sqlite_pedido_model import SqlitePedidoModel, SqlitePedidoItemModel
from backend.infra.db import get_db

class SqlitePedidoRepository(PedidoRepository):
    def get_open_pedido(self, usuario_id: int) -> Pedido:
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM Pedidos WHERE UsuarioId = ? AND Status = 'ABERTO' ORDER BY Id DESC LIMIT 1",
                (usuario_id,),
            ).fetchone()
            return SqlitePedidoModel.to_entity(row)

    def save_pedido(self, pedido: Pedido) -> int:
        with get_db() as conn:
            cur = conn.execute(
                "INSERT INTO Pedidos (UsuarioId, Status) VALUES (?, 'ABERTO')",
                (pedido.usuario_id,),
            )
            conn.commit()
            return cur.lastrowid

    def save_item(self, item: PedidoItem) -> None:
        with get_db() as conn:
            conn.execute(
                """
                    INSERT INTO PedidoItens (PedidoId, ItemNome, ItemFoto, ItemValor, Quantidade, Observacao)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (item.pedido_id, item.item_nome, item.item_foto, float(item.item_valor), int(item.quantidade), item.observacao),
            )
            conn.commit()

    def get_open_pedido_items(self, usuario_id: int) -> List[PedidoItem]:
        with get_db() as conn:
            rows = conn.execute(
                """
                SELECT pi.Id,
                       pi.PedidoId,
                       pi.ItemNome,
                       pi.ItemFoto,
                       pi.ItemValor,
                       pi.Quantidade,
                       pi.Observacao,
                       pi.CriadoEm
                FROM PedidoItens pi
                JOIN Pedidos p ON p.Id = pi.PedidoId
                WHERE p.UsuarioId = ? AND p.Status = 'ABERTO'
                ORDER BY pi.Id DESC
                """,
                (usuario_id,),
            ).fetchall()
            return [SqlitePedidoItemModel.to_entity(r) for r in rows]

    def delete_item_from_open_pedido(self, pedido_item_id: int, usuario_id: int) -> None:
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

    def finalize_open_pedido(self, usuario_id: int) -> None:
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

    def get_finalized_pedidos(self, usuario_id: int) -> List[Pedido]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM Pedidos WHERE UsuarioId = ? AND Status = 'FINALIZADO' ORDER BY Id DESC",
                (usuario_id,)
            ).fetchall()
            return [SqlitePedidoModel.to_entity(r) for r in rows]

    def get_pedido_items(self, pedido_id: int) -> List[PedidoItem]:
        with get_db() as conn:
            rows = conn.execute(
                """
                SELECT pi.Id,
                       pi.PedidoId,
                       pi.ItemNome,
                       pi.ItemFoto,
                       pi.ItemValor,
                       pi.Quantidade,
                       pi.Observacao,
                       pi.CriadoEm
                FROM PedidoItens pi
                WHERE pi.PedidoId = ?
                ORDER BY pi.Id DESC
                """,
                (pedido_id,)
            ).fetchall()
            return [SqlitePedidoItemModel.to_entity(r) for r in rows]
