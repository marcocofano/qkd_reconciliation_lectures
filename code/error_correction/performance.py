import logging
import time
import pprint
from error_correction.channels import Channel
from error_correction.decoders import BPA
from error_correction.utils import DelayedInterrupt
from error_correction.plotter import Plotter

from error_correction.outputs import StatusDecodingPerformance

def decoding_performance(
    channel_class: Channel,
    decoder: BPA,
    code,
    params,
    data_dirs,
    min_fec=100,
    log_freq=5,
    logger=logging.getLogger(),
):
    # id_keys = ["channel", "code", "decoder", "codeword", "min_fec"] + dec_fac.id_keys
    # id_val = [vars(args)[key] for key in id_keys]
    code_n = code.get_n()
    x = code.parity_mtx[0] * 0
    # TODO: allow for random input

    # if codeword == -1
    #     x = code.cb[np.random.choice(code.cb.shape[0], 1)[0]]
    # saver = utils.Saver(args.data_dir, list(zip(id_keys, id_val)))
    plotter = Plotter(data_dirs=data_dirs)

    status = StatusDecodingPerformance(
        channel=channel_class.name,
        code=code.config.get_slug(),
        decoder=decoder.name,
        max_iter=decoder.max_iter,
        data_dirs=data_dirs,
    )

    for param in params:
        logger.info("Starting parameter: %f" % param)

        tot, fec, fer, bec, ber = 0, 0, 0.0, 0, 0.0
        start_time = time.time()

        def log_status():
            keys = ["tot", "fec", "fer", "bec", "ber"]
            vals = [int(tot), int(fec), float(fer), int(bec), float(ber)]
            logger.info(
                ", ".join(
                    ("%s:%s" % (key.upper(), val) for key, val in zip(keys, vals))
                )
            )

        channel = channel_class(param=param)

        with DelayedInterrupt(logger) as catcher:
            while fec < min_fec:
                y = channel.send(x)
                llrs = channel.llrs(y)
                x_hat, n_iter, decoded = decoder.decode(y, llrs)
                errors = (~(x == x_hat)).sum()
                fec += errors > 0
                bec += errors
                tot += 1
                fer, ber = fec / tot, bec / (tot * code_n)
                if time.time() - start_time > log_freq:
                    start_time = time.time()
                    log_status()

                if catcher.stop_signal:
                    logger.warning("Exiting early")
                    status.update_metrics(
                        channel_parameter=param,
                        metrics={
                            "tot": int(tot),
                            "bec": int(bec),
                            "ber": float(ber),
                            "fec": int(fec),
                            "fer": float(fer),
                        },
                    )
                    break

        log_status()
        status.update_metrics(
            channel_parameter=param,
            metrics={
                "tot": int(tot),
                "bec": int(bec),
                "ber": float(ber),
                "fec": int(fec),
                "fer": float(fer),
            },
        )
        logger.debug(pprint.pformat(status.get_status_dict()))

    status.save_json()
    plotter.plot(status)
    logger.info("Done!")
